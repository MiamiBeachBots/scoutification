#!/usr/bin/env python3
"""
FRC Scouting Dashboard — 2026 REBUILT
Streamlit dashboard for pick lists, team analysis, match prediction, and raw data.
"""

import streamlit as st
import pandas as pd
import sqlite3
import altair as alt
import os


class ScoutingDashboard:
    def __init__(self, db_path=None):
        self.db_path = db_path or os.getenv('DB_PATH', 'scouting_data.db')

    # ──────────────────────────────────────────────────────────────
    # Data Loaders
    # ──────────────────────────────────────────────────────────────

    def load_data(self):
        """Per-team aggregate stats for pick list / analysis."""
        try:
            conn = sqlite3.connect(self.db_path)
            query = """
            SELECT
                team_number,
                COUNT(*) AS Matches_Played,

                AVG(auto_fuel_active_hub)  AS Avg_Auto_Fuel,
                AVG(CASE WHEN auto_tower_level1 = 1 THEN 1.0 ELSE 0.0 END) AS Auto_Tower_Rate,

                AVG(teleop_fuel_active_hub)   AS Avg_Teleop_Active,
                AVG(teleop_fuel_inactive_hub) AS Avg_Teleop_Inactive,
                AVG(auto_fuel_active_hub + teleop_fuel_active_hub) AS Avg_Total_Active_Hub,

                AVG(CASE max_tower_level
                    WHEN 'Level 3' THEN 3.0
                    WHEN 'Level 2' THEN 2.0
                    WHEN 'Level 1' THEN 1.0
                    ELSE 0.0
                END) AS Avg_Tower_Level,

                AVG(minor_fouls + major_fouls * 3) AS Avg_Foul_Points,

                AVG(CASE WHEN energized_rp    = 1 THEN 1.0 ELSE 0.0 END) AS Energized_Rate,
                AVG(CASE WHEN supercharged_rp = 1 THEN 1.0 ELSE 0.0 END) AS Supercharged_Rate,
                AVG(CASE WHEN traversal_rp    = 1 THEN 1.0 ELSE 0.0 END) AS Traversal_Rate
            FROM scouting_data
            GROUP BY team_number
            ORDER BY team_number
            """
            df = pd.read_sql_query(query, conn)
            conn.close()
            return df
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return pd.DataFrame()

    def load_raw_data(self):
        try:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query(
                "SELECT * FROM scouting_data ORDER BY match_number, team_number", conn
            )
            conn.close()
            return df
        except Exception as e:
            st.error(f"Error loading raw data: {e}")
            return pd.DataFrame()

    def load_team_match_data(self, team_number):
        try:
            conn = sqlite3.connect(self.db_path)
            query = """
            SELECT
                match_number,
                auto_fuel_active_hub,
                teleop_fuel_active_hub,
                teleop_fuel_inactive_hub,
                (auto_fuel_active_hub + teleop_fuel_active_hub) AS total_active_hub,
                CASE max_tower_level
                    WHEN 'Level 3' THEN 3
                    WHEN 'Level 2' THEN 2
                    WHEN 'Level 1' THEN 1
                    ELSE 0
                END AS tower_level_num,
                minor_fouls,
                major_fouls
            FROM scouting_data
            WHERE team_number = ?
            ORDER BY match_number
            """
            df = pd.read_sql_query(query, conn, params=[team_number])
            conn.close()
            return df
        except Exception as e:
            st.error(f"Error loading team data: {e}")
            return pd.DataFrame()

    # ──────────────────────────────────────────────────────────────
    # Pick List Tab
    # ──────────────────────────────────────────────────────────────

    def pick_list_formulation_tab(self):
        st.header("🎯 Pick List Formulation")
        st.markdown("Weighted team rankings for alliance selection.")

        df = self.load_data()
        if df.empty:
            st.warning("No scouting data yet. Scan some QR codes first!")
            return

        st.sidebar.header("⚖️ Scoring Weights")

        auto_w     = st.sidebar.slider("Auto FUEL",          0.0, 5.0, 1.5, 0.1)
        teleop_w   = st.sidebar.slider("Teleop Active HUB",  0.0, 5.0, 2.0, 0.1)
        tower_w    = st.sidebar.slider("Tower Level",         0.0, 5.0, 1.5, 0.1)
        foul_w     = st.sidebar.slider("Foul Penalty (neg)",  0.0, 3.0, 1.0, 0.1)

        df['Weighted_Score'] = (
            df['Avg_Auto_Fuel']        * auto_w   +
            df['Avg_Teleop_Active']    * teleop_w +
            df['Avg_Tower_Level']      * tower_w  -
            df['Avg_Foul_Points']      * foul_w
        )

        df = df.sort_values('Weighted_Score', ascending=False).reset_index(drop=True)

        if 'dnp_teams' not in st.session_state:
            st.session_state.dnp_teams = set()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Teams Scouted", len(df))
        col2.metric("Energized RP% (avg)", f"{df['Energized_Rate'].mean()*100:.0f}%")
        col3.metric("Supercharged RP% (avg)", f"{df['Supercharged_Rate'].mean()*100:.0f}%")
        col4.metric("Traversal RP% (avg)", f"{df['Traversal_Rate'].mean()*100:.0f}%")

        st.markdown("---")
        st.subheader("📊 Team Rankings")

        # Header row
        hcols = st.columns([0.4, 0.4, 1.0, 0.9, 0.9, 0.9, 0.9, 0.9, 0.6])
        for col, label in zip(hcols, ["DNP","#","Team","Avg Auto","Avg Tel.act","Avg Tower","Fouls(pts)","Score","Matches"]):
            col.markdown(f"**{label}**")

        for idx, row in df.iterrows():
            team  = row['team_number']
            rank  = idx + 1
            emoji = "🥇" if rank <= 8 else ("🥈" if rank <= 24 else "")

            cols = st.columns([0.4, 0.4, 1.0, 0.9, 0.9, 0.9, 0.9, 0.9, 0.6])
            with cols[0]:
                is_dnp = st.checkbox("", value=team in st.session_state.dnp_teams,
                                     key=f"dnp_{team}_{idx}", help=f"DNP Team {team}")
                if is_dnp: st.session_state.dnp_teams.add(team)
                else:      st.session_state.dnp_teams.discard(team)
            cols[1].markdown(f"{emoji} **{rank}**")
            label_html = (f"<span style='text-decoration:line-through;color:gray'>Team {team}</span>"
                          if team in st.session_state.dnp_teams else f"**Team {team}**")
            cols[2].markdown(label_html, unsafe_allow_html=True)
            cols[3].text(f"{row['Avg_Auto_Fuel']:.1f}")
            cols[4].text(f"{row['Avg_Teleop_Active']:.1f}")
            cols[5].text(f"{row['Avg_Tower_Level']:.2f}")
            cols[6].text(f"{row['Avg_Foul_Points']:.1f}")
            cols[7].text(f"{row['Weighted_Score']:.2f}")
            cols[8].text(int(row['Matches_Played']))

        st.markdown("---")
        if st.button("📥 Export Pick List (excluding DNP)"):
            export = df[~df['team_number'].isin(st.session_state.dnp_teams)]
            st.download_button("Download CSV", export.to_csv(index=False),
                               "pick_list.csv", "text/csv")

    # ──────────────────────────────────────────────────────────────
    # Team Analysis Tab
    # ──────────────────────────────────────────────────────────────

    def team_analysis_tab(self):
        st.header("📊 Team Analysis")

        df = self.load_data()
        if df.empty:
            st.warning("No scouting data yet.")
            return

        team = st.sidebar.selectbox("Select Team",
                                    sorted(df['team_number'].tolist()))
        stats = df[df['team_number'] == team].iloc[0]

        st.subheader(f"Team {int(team)}")
        st.markdown(f"**Matches scouted:** {int(stats['Matches_Played'])}")
        st.markdown("---")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Avg Auto FUEL",      f"{stats['Avg_Auto_Fuel']:.1f}")
        c2.metric("Avg Teleop Active",   f"{stats['Avg_Teleop_Active']:.1f}")
        c3.metric("Avg Tower Level",     f"{stats['Avg_Tower_Level']:.2f}")
        c4.metric("Auto Tower Rate",     f"{stats['Auto_Tower_Rate']*100:.0f}%")

        c5, c6, c7, c8 = st.columns(4)
        c5.metric("Avg Teleop Inactive", f"{stats['Avg_Teleop_Inactive']:.1f}")
        c6.metric("Energized RP%",       f"{stats['Energized_Rate']*100:.0f}%")
        c7.metric("Supercharged RP%",    f"{stats['Supercharged_Rate']*100:.0f}%")
        c8.metric("Traversal RP%",       f"{stats['Traversal_Rate']*100:.0f}%")

        st.markdown("---")

        match_data = self.load_team_match_data(team)
        if not match_data.empty:
            st.subheader("📈 FUEL Scored Per Match")
            melted = match_data[['match_number', 'auto_fuel_active_hub',
                                  'teleop_fuel_active_hub', 'teleop_fuel_inactive_hub']].melt(
                id_vars='match_number', var_name='Period', value_name='FUEL'
            )
            melted['Period'] = melted['Period'].map({
                'auto_fuel_active_hub':    'Auto (Active HUB)',
                'teleop_fuel_active_hub':  'Teleop (Active HUB)',
                'teleop_fuel_inactive_hub':'Teleop (Inactive HUB)',
            })
            chart = alt.Chart(melted).mark_line(point=True).encode(
                x=alt.X('match_number:Q', title='Match'),
                y=alt.Y('FUEL:Q', title='FUEL Scored'),
                color=alt.Color('Period:N'),
                tooltip=['match_number', 'Period', 'FUEL']
            ).properties(height=350).interactive()
            st.altair_chart(chart, use_container_width=True)

            st.subheader("🏗️ TOWER Level Per Match")
            tower_chart = alt.Chart(match_data).mark_bar().encode(
                x=alt.X('match_number:Q', title='Match'),
                y=alt.Y('tower_level_num:Q', title='Tower Level', scale=alt.Scale(domain=[0, 3])),
                color=alt.Color('tower_level_num:Q', scale=alt.Scale(scheme='blues')),
                tooltip=['match_number', 'tower_level_num']
            ).properties(height=200)
            st.altair_chart(tower_chart, use_container_width=True)

    # ──────────────────────────────────────────────────────────────
    # Match Predictor Tab
    # ──────────────────────────────────────────────────────────────

    def match_predictor_tab(self):
        st.header("🔮 Match Predictor")
        st.markdown("Predicts match outcome based on scouted team averages.")

        df = self.load_data()
        if df.empty:
            st.warning("No scouting data yet.")
            return

        teams = sorted(df['team_number'].tolist())
        if len(teams) < 6:
            st.warning(f"Need at least 6 scouted teams. Have {len(teams)}.")
            return

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🔴 Red Alliance")
            red = st.multiselect("Red teams", teams, max_selections=3, key="red")
        with col2:
            st.subheader("🔵 Blue Alliance")
            blue = st.multiselect("Blue teams", [t for t in teams if t not in red],
                                  max_selections=3, key="blue")

        if len(red) == 3 and len(blue) == 3:
            st.markdown("---")

            def alliance_score(team_list):
                rows = df[df['team_number'].isin(team_list)]
                active_hub  = rows['Avg_Total_Active_Hub'].sum()
                tower       = rows['Avg_Tower_Level'].sum()
                fouls       = rows['Avg_Foul_Points'].sum()
                # Rough REBUILT scoring: active hub FUEL + tower contributions
                score = active_hub + (tower * 15) - fouls
                return score, active_hub, tower, fouls

            r_score, r_hub, r_tower, r_fouls = alliance_score(red)
            b_score, b_hub, b_tower, b_fouls = alliance_score(blue)

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("🔴 Red")
                for t in red:
                    row = df[df['team_number'] == t].iloc[0]
                    st.markdown(f"**{int(t)}:** Active HUB avg {row['Avg_Total_Active_Hub']:.1f}, "
                                f"Tower {row['Avg_Tower_Level']:.1f}")
                st.metric("Expected Score", f"{r_score:.1f}")
                st.metric("Avg Active HUB FUEL", f"{r_hub:.0f}")
                energized  = "✅" if r_hub >= 100 else "❌"
                supercharged = "✅" if r_hub >= 360 else "❌"
                st.markdown(f"ENERGIZED RP likely: {energized} &nbsp; SUPERCHARGED RP likely: {supercharged}")
            with col2:
                st.subheader("🔵 Blue")
                for t in blue:
                    row = df[df['team_number'] == t].iloc[0]
                    st.markdown(f"**{int(t)}:** Active HUB avg {row['Avg_Total_Active_Hub']:.1f}, "
                                f"Tower {row['Avg_Tower_Level']:.1f}")
                st.metric("Expected Score", f"{b_score:.1f}")
                st.metric("Avg Active HUB FUEL", f"{b_hub:.0f}")
                energized  = "✅" if b_hub >= 100 else "❌"
                supercharged = "✅" if b_hub >= 360 else "❌"
                st.markdown(f"ENERGIZED RP likely: {energized} &nbsp; SUPERCHARGED RP likely: {supercharged}")

            st.markdown("---")
            total = r_score + b_score
            r_pct = (r_score / total * 100) if total > 0 else 50
            b_pct = 100 - r_pct

            winner = "🔴 Red Alliance" if r_score > b_score else ("🔵 Blue Alliance" if b_score > r_score else "⚪ Tie")
            st.subheader(f"🏆 {winner}")

            prob = pd.DataFrame({'Alliance': ['Red', 'Blue'], 'Probability': [r_pct, b_pct], 'Color': ['red', 'blue']})
            st.altair_chart(
                alt.Chart(prob).mark_bar().encode(
                    x=alt.X('Probability:Q', scale=alt.Scale(domain=[0, 100]), title='Win Probability (%)'),
                    y=alt.Y('Alliance:N', title=''),
                    color=alt.Color('Color:N', scale=alt.Scale(domain=['red','blue'], range=['#ff4444','#4444ff']), legend=None),
                    tooltip=['Alliance', alt.Tooltip('Probability:Q', format='.1f')]
                ).properties(height=150),
                use_container_width=True
            )
        elif red or blue:
            st.info("Select exactly 3 teams per alliance.")

    # ──────────────────────────────────────────────────────────────
    # Raw Data Tab
    # ──────────────────────────────────────────────────────────────

    def raw_data_tab(self):
        st.header("📄 Raw Data")
        df = self.load_raw_data()
        if df.empty:
            st.warning("No scouting data yet.")
            return

        c1, c2, c3 = st.columns(3)
        c1.metric("Records", len(df))
        c2.metric("Teams",   df['team_number'].nunique())
        c3.metric("Matches", df['match_number'].nunique())

        st.markdown("---")
        st.download_button("📥 Download CSV", df.to_csv(index=False),
                           "scouting_data_rebuilt_2026.csv", "text/csv")
        st.markdown("---")
        st.dataframe(df, use_container_width=True, hide_index=True,
                     column_config={
                         "match_number":             st.column_config.NumberColumn("Match #"),
                         "team_number":              st.column_config.NumberColumn("Team #"),
                         "alliance":                 st.column_config.TextColumn("Alliance"),
                         "scouter_name":             st.column_config.TextColumn("Scouter"),
                         "pre_loaded_fuel":          st.column_config.NumberColumn("Pre-load"),
                         "auto_fuel_active_hub":     st.column_config.NumberColumn("Auto Fuel"),
                         "auto_tower_level1":        st.column_config.NumberColumn("Auto Twr L1"),
                         "teleop_fuel_active_hub":   st.column_config.NumberColumn("TP Active"),
                         "teleop_fuel_inactive_hub": st.column_config.NumberColumn("TP Inactive"),
                         "fuel_collection_source":   st.column_config.TextColumn("Collection"),
                         "max_tower_level":          st.column_config.TextColumn("Tower"),
                         "minor_fouls":              st.column_config.NumberColumn("Minor Fouls"),
                         "major_fouls":              st.column_config.NumberColumn("Major Fouls"),
                         "energized_rp":             st.column_config.NumberColumn("Energized"),
                         "supercharged_rp":          st.column_config.NumberColumn("Supercharged"),
                         "traversal_rp":             st.column_config.NumberColumn("Traversal"),
                     })


def main():
    st.set_page_config(
        page_title="FRC Scouting – REBUILT 2026",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.title("⚡ FRC Scouting Dashboard — REBUILT 2026")

    dash = ScoutingDashboard()
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎯 Pick List", "📊 Team Analysis", "🔮 Match Predictor", "📄 Raw Data"
    ])
    with tab1: dash.pick_list_formulation_tab()
    with tab2: dash.team_analysis_tab()
    with tab3: dash.match_predictor_tab()
    with tab4: dash.raw_data_tab()


if __name__ == '__main__':
    main()
