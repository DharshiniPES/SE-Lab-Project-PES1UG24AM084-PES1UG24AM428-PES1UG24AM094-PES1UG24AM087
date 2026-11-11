"""
Generator for docs/jira_dashboard.html
Creates an authentic, interactive Atlassian Jira Software dashboard representation
for the Digital Campus Library Reservation Gateway (LRG) project.
Zero emojis, 100% self-contained HTML/CSS/JS.
"""

import json
import os

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jira Software - Digital Campus Library Reservation Gateway (LRG)</title>
    <style>
        :root {
            --jira-blue: #0052cc;
            --jira-dark-blue: #0747a6;
            --jira-navy: #172b4d;
            --jira-subtle-text: #5e6c84;
            --jira-bg: #f4f5f7;
            --jira-card-bg: #ffffff;
            --jira-border: #dfe1e6;
            --jira-hover: #ebecf0;
            --jira-green: #00875a;
            --jira-green-bg: #e3fcef;
            --jira-orange: #ffab00;
            --jira-orange-bg: #fff0b3;
            --jira-red: #de350b;
            --jira-red-bg: #ffebe6;
            --jira-purple: #5243aa;
            --jira-purple-bg: #eae6ff;
            --jira-teal: #008da6;
            --jira-teal-bg: #e6fcff;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
            background-color: var(--jira-bg);
            color: var(--jira-navy);
            line-height: 1.4;
            font-size: 14px;
        }

        /* Top Jira Global Navigation Bar */
        .jira-nav {
            background-color: #0c66e4;
            color: #ffffff;
            height: 48px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 16px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.15);
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .jira-nav-left {
            display: flex;
            align-items: center;
            gap: 16px;
        }

        .jira-logo {
            font-size: 16px;
            font-weight: 700;
            letter-spacing: -0.2px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .jira-logo-badge {
            background: rgba(255, 255, 255, 0.25);
            padding: 2px 6px;
            border-radius: 3px;
            font-size: 11px;
            text-transform: uppercase;
            font-weight: 800;
        }

        .jira-nav-menu {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .jira-nav-item {
            color: rgba(255, 255, 255, 0.9);
            padding: 6px 12px;
            border-radius: 3px;
            font-size: 13px;
            font-weight: 500;
            text-decoration: none;
            cursor: pointer;
        }

        .jira-nav-item:hover, .jira-nav-item.active {
            background: rgba(255, 255, 255, 0.15);
            color: #ffffff;
        }

        .jira-nav-right {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .jira-search-box {
            background: rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 4px;
            padding: 4px 10px;
            color: #ffffff;
            font-size: 12px;
            width: 220px;
        }

        .jira-search-box::placeholder {
            color: rgba(255, 255, 255, 0.7);
        }

        .jira-user-pill {
            background: #ffffff;
            color: #0c66e4;
            font-weight: 700;
            border-radius: 50%;
            width: 28px;
            height: 28px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
        }

        /* Project Subheader */
        .project-header {
            background: #ffffff;
            border-bottom: 1px solid var(--jira-border);
            padding: 16px 24px;
        }

        .breadcrumb {
            font-size: 12px;
            color: var(--jira-subtle-text);
            margin-bottom: 6px;
        }

        .breadcrumb a {
            color: var(--jira-blue);
            text-decoration: none;
        }

        .project-title-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
        }

        .project-title {
            font-size: 22px;
            font-weight: 600;
            color: var(--jira-navy);
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .project-key-tag {
            background: var(--jira-hover);
            color: var(--jira-subtle-text);
            font-size: 12px;
            padding: 3px 8px;
            border-radius: 3px;
            font-weight: 600;
        }

        .project-meta-badges {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }

        .meta-badge {
            font-size: 12px;
            padding: 4px 10px;
            border-radius: 12px;
            font-weight: 500;
            border: 1px solid var(--jira-border);
            background: var(--jira-bg);
        }

        .meta-badge-success {
            background: var(--jira-green-bg);
            color: var(--jira-green);
            border-color: #abf5d1;
            font-weight: 600;
        }

        /* View Navigation Tabs */
        .jira-tabs {
            display: flex;
            gap: 24px;
            margin-top: 16px;
            border-bottom: 2px solid transparent;
        }

        .jira-tab {
            padding: 8px 4px;
            font-size: 14px;
            font-weight: 600;
            color: var(--jira-subtle-text);
            cursor: pointer;
            border-bottom: 2px solid transparent;
            margin-bottom: -1px;
            text-decoration: none;
        }

        .jira-tab:hover {
            color: var(--jira-blue);
        }

        .jira-tab.active {
            color: var(--jira-blue);
            border-bottom-color: var(--jira-blue);
        }

        /* Control / Filter Bar */
        .filter-bar {
            background: #ffffff;
            padding: 12px 24px;
            border-bottom: 1px solid var(--jira-border);
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 12px;
        }

        .filter-group {
            display: flex;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
        }

        .filter-label {
            font-size: 12px;
            font-weight: 600;
            color: var(--jira-subtle-text);
            text-transform: uppercase;
        }

        .filter-btn {
            background: var(--jira-bg);
            border: 1px solid var(--jira-border);
            border-radius: 3px;
            padding: 5px 12px;
            font-size: 12px;
            font-weight: 500;
            cursor: pointer;
            color: var(--jira-navy);
            transition: all 0.15s ease;
        }

        .filter-btn:hover {
            background: var(--jira-hover);
        }

        .filter-btn.active {
            background: var(--jira-blue);
            color: #ffffff;
            border-color: var(--jira-blue);
        }

        /* Main Container */
        .main-container {
            padding: 20px 24px;
            min-height: calc(100vh - 180px);
        }

        .tab-content {
            display: none;
        }

        .tab-content.active {
            display: block;
        }

        /* Kanban Board Columns */
        .board-grid {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 16px;
            align-items: start;
        }

        @media (max-width: 1200px) {
            .board-grid {
                grid-template-columns: repeat(2, 1fr);
            }
        }

        @media (max-width: 768px) {
            .board-grid {
                grid-template-columns: 1fr;
            }
        }

        .board-column {
            background: #ebecf0;
            border-radius: 6px;
            padding: 10px;
            min-height: 480px;
            display: flex;
            flex-direction: column;
        }

        .column-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 6px 8px 10px;
            font-size: 12px;
            font-weight: 700;
            color: var(--jira-subtle-text);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .column-counter {
            background: rgba(9, 30, 66, 0.08);
            color: var(--jira-navy);
            padding: 2px 7px;
            border-radius: 10px;
            font-size: 11px;
        }

        .card-list {
            display: flex;
            flex-direction: column;
            gap: 8px;
            flex-grow: 1;
        }

        .empty-column-placeholder {
            border: 2px dashed #c1c7d0;
            border-radius: 4px;
            padding: 20px 10px;
            text-align: center;
            color: var(--jira-subtle-text);
            font-size: 12px;
            font-style: italic;
        }

        /* Issue Card */
        .jira-card {
            background: var(--jira-card-bg);
            border-radius: 4px;
            padding: 12px;
            box-shadow: 0 1px 2px rgba(9, 30, 66, 0.15);
            cursor: pointer;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
            border: 1px solid transparent;
        }

        .jira-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(9, 30, 66, 0.2);
            border-color: var(--jira-border);
        }

        .card-epic-tag {
            display: inline-block;
            font-size: 10px;
            font-weight: 700;
            padding: 2px 6px;
            border-radius: 3px;
            text-transform: uppercase;
            margin-bottom: 6px;
            letter-spacing: 0.3px;
        }

        .epic-catalog { background: var(--jira-purple-bg); color: var(--jira-purple); }
        .epic-fines { background: var(--jira-teal-bg); color: var(--jira-teal); }
        .epic-admin { background: var(--jira-orange-bg); color: #974f00; }
        .epic-sec { background: #deebff; color: #0747a6; }

        .card-summary {
            font-size: 13px;
            font-weight: 600;
            color: var(--jira-navy);
            margin-bottom: 8px;
            line-height: 1.35;
        }

        .card-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 11px;
            margin-top: 8px;
            padding-top: 8px;
            border-top: 1px solid #f4f5f7;
        }

        .card-meta-left {
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .issue-type-tag {
            font-size: 10px;
            font-weight: 700;
            padding: 1px 4px;
            border-radius: 2px;
            background: #e3fcef;
            color: #006644;
        }

        .card-key {
            color: var(--jira-blue);
            font-weight: 600;
        }

        .card-meta-right {
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .sp-badge {
            background: #ebecf0;
            color: var(--jira-navy);
            font-weight: 700;
            font-size: 11px;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .assignee-avatar {
            width: 24px;
            height: 24px;
            border-radius: 50%;
            background: var(--jira-blue);
            color: #ffffff;
            font-weight: 700;
            font-size: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-transform: uppercase;
        }

        .avatar-dv { background: #0052cc; }
        .avatar-dg { background: #00875a; }
        .avatar-dy { background: #5243aa; }
        .avatar-dt { background: #ff8b00; }

        /* Backlog Accordions */
        .sprint-block {
            background: #ffffff;
            border: 1px solid var(--jira-border);
            border-radius: 6px;
            margin-bottom: 20px;
            overflow: hidden;
        }

        .sprint-header {
            background: #f4f5f7;
            padding: 14px 20px;
            border-bottom: 1px solid var(--jira-border);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
        }

        .sprint-title-area {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .sprint-title {
            font-size: 16px;
            font-weight: 700;
            color: var(--jira-navy);
        }

        .sprint-dates {
            font-size: 12px;
            color: var(--jira-subtle-text);
        }

        .sprint-stats {
            display: flex;
            gap: 8px;
            align-items: center;
        }

        .sprint-pill {
            font-size: 11px;
            font-weight: 600;
            padding: 3px 8px;
            border-radius: 3px;
        }

        .pill-done { background: var(--jira-green-bg); color: var(--jira-green); }
        .pill-sp { background: #dfe1e6; color: var(--jira-navy); }

        .backlog-table {
            width: 100%;
            border-collapse: collapse;
        }

        .backlog-table th {
            background: #fafbfc;
            text-align: left;
            padding: 8px 16px;
            font-size: 11px;
            font-weight: 700;
            color: var(--jira-subtle-text);
            text-transform: uppercase;
            border-bottom: 1px solid var(--jira-border);
        }

        .backlog-table td {
            padding: 10px 16px;
            border-bottom: 1px solid #f0f1f4;
            font-size: 13px;
        }

        .backlog-table tr:hover {
            background-color: #f7f9fa;
            cursor: pointer;
        }

        /* Burndown Chart */
        .burndown-card {
            background: #ffffff;
            border: 1px solid var(--jira-border);
            border-radius: 6px;
            padding: 24px;
            margin-bottom: 24px;
        }

        .burndown-title-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
            flex-wrap: wrap;
            gap: 12px;
        }

        .burndown-chart-wrapper {
            position: relative;
            margin: 20px 0;
            background: #fafbfc;
            border: 1px solid var(--jira-border);
            border-radius: 6px;
            padding: 20px;
        }

        .burndown-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 16px;
            font-size: 12px;
        }

        .burndown-table th, .burndown-table td {
            border: 1px solid var(--jira-border);
            padding: 8px 12px;
            text-align: left;
        }

        .burndown-table th {
            background: var(--jira-bg);
            font-weight: 600;
        }

        /* Velocity and Stats */
        .velocity-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
            margin-bottom: 24px;
        }

        @media (max-width: 900px) {
            .velocity-grid {
                grid-template-columns: 1fr;
            }
        }

        .velocity-card {
            background: #ffffff;
            border: 1px solid var(--jira-border);
            border-radius: 6px;
            padding: 18px;
        }

        .velocity-num {
            font-size: 32px;
            font-weight: 700;
            color: var(--jira-blue);
            margin: 6px 0;
        }

        .velocity-label {
            font-size: 12px;
            color: var(--jira-subtle-text);
            text-transform: uppercase;
            font-weight: 600;
        }

        /* Modal Dialog */
        .jira-modal-backdrop {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(9, 30, 66, 0.54);
            z-index: 1000;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .jira-modal {
            background: #ffffff;
            border-radius: 6px;
            max-width: 800px;
            width: 100%;
            max-height: 90vh;
            overflow-y: auto;
            box-shadow: 0 8px 24px rgba(9, 30, 66, 0.25);
            display: flex;
            flex-direction: column;
        }

        .modal-header {
            padding: 16px 24px;
            border-bottom: 1px solid var(--jira-border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .modal-close-btn {
            background: none;
            border: none;
            font-size: 20px;
            cursor: pointer;
            color: var(--jira-subtle-text);
            padding: 4px 8px;
        }

        .modal-body {
            padding: 24px;
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 24px;
        }

        @media (max-width: 700px) {
            .modal-body {
                grid-template-columns: 1fr;
            }
        }

        .modal-left h3 {
            font-size: 18px;
            margin-bottom: 12px;
            color: var(--jira-navy);
        }

        .modal-section-title {
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            color: var(--jira-subtle-text);
            margin: 16px 0 6px;
        }

        .modal-desc-box {
            background: #fafbfc;
            border: 1px solid var(--jira-border);
            border-radius: 4px;
            padding: 12px;
            font-size: 13px;
            line-height: 1.5;
        }

        .modal-attr-group {
            margin-bottom: 12px;
        }

        .attr-label {
            font-size: 11px;
            font-weight: 600;
            color: var(--jira-subtle-text);
            text-transform: uppercase;
            margin-bottom: 2px;
        }

        .attr-value {
            font-size: 13px;
            font-weight: 500;
        }

        /* SVG Chart Styling */
        .chart-svg {
            width: 100%;
            height: 280px;
        }

        .chart-line-ideal {
            stroke: #c1c7d0;
            stroke-width: 2;
            stroke-dasharray: 4, 4;
            fill: none;
        }

        .chart-line-actual {
            stroke: #0052cc;
            stroke-width: 3;
            fill: none;
        }

        .chart-point {
            fill: #0052cc;
            stroke: #ffffff;
            stroke-width: 2;
        }

        .chart-text {
            font-size: 11px;
            fill: var(--jira-subtle-text);
        }
    </style>
</head>
<body>

    <!-- Jira Global Navigation -->
    <header class="jira-nav">
        <div class="jira-nav-left">
            <div class="jira-logo">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M11.53 2C6.45 2 2.3 6.01 2 11.04C3.89 10.6 5.67 9.8 7.27 8.7C8.87 7.6 10.3 6.2 11.53 2Z" fill="#ffffff" fill-opacity="0.9"/>
                    <path d="M12.47 2C17.55 2 21.7 6.01 22 11.04C20.11 10.6 18.33 9.8 16.73 8.7C15.13 7.6 13.7 6.2 12.47 2Z" fill="#ffffff"/>
                    <path d="M12 13C12 17.97 7.97 22 3 22C4.1 20.3 5.5 18.87 7.2 17.8C8.9 16.73 10.8 16.1 12 13Z" fill="#ffffff" fill-opacity="0.7"/>
                </svg>
                <span>Jira Software</span>
                <span class="jira-logo-badge">Cloud</span>
            </div>
            <nav class="jira-nav-menu">
                <span class="jira-nav-item active">Projects</span>
                <span class="jira-nav-item">Filters</span>
                <span class="jira-nav-item">Dashboards</span>
                <span class="jira-nav-item">Teams</span>
            </nav>
        </div>
        <div class="jira-nav-right">
            <input type="text" id="searchInput" class="jira-search-box" placeholder="Search issues (e.g. LRG-301)..." onkeyup="filterBySearch()">
            <div class="jira-user-pill" title="Current User: Dharshini V (PES1UG24AM428)">DV</div>
        </div>
    </header>

    <!-- Project Header -->
    <section class="project-header">
        <div class="breadcrumb">
            <a href="#">Projects</a> / <a href="#">Engineering</a> / <span>Digital Campus Library Reservation Gateway</span>
        </div>
        <div class="project-title-row">
            <div class="project-title">
                Digital Campus Library Reservation Gateway
                <span class="project-key-tag">LRG</span>
            </div>
            <div class="project-meta-badges">
                <span class="meta-badge">Scrum Framework</span>
                <span class="meta-badge">Lead: Dhareen G (PES1UG24AM084)</span>
                <span class="meta-badge">Dev Lead: Dharshini V (PES1UG24AM428)</span>
                <span class="meta-badge meta-badge-success">Sprints 1-3 Completed (85 SP / 85 SP)</span>
            </div>
        </div>

        <!-- Navigation Tabs -->
        <div class="jira-tabs">
            <div class="jira-tab active" onclick="switchTab('boardTab', this)">Active Sprint Board</div>
            <div class="jira-tab" onclick="switchTab('backlogTab', this)">Backlog & Sprints</div>
            <div class="jira-tab" onclick="switchTab('burndownTab', this)">Sprint-3 Burndown Chart</div>
            <div class="jira-tab" onclick="switchTab('velocityTab', this)">Velocity & Epics</div>
            <div class="jira-tab" onclick="switchTab('traceabilityTab', this)">SRS Traceability Matrix</div>
        </div>
    </section>

    <!-- Filter Bar -->
    <section class="filter-bar">
        <div class="filter-group">
            <span class="filter-label">Quick Filters:</span>
            <button class="filter-btn active" onclick="setSprintFilter('all', this)">All Sprints</button>
            <button class="filter-btn" onclick="setSprintFilter('sprint-3', this)">Sprint 3 (Spill-overs & QA)</button>
            <button class="filter-btn" onclick="setSprintFilter('sprint-2', this)">Sprint 2 (Holds & Admin)</button>
            <button class="filter-btn" onclick="setSprintFilter('sprint-1', this)">Sprint 1 (Search & Auth)</button>
        </div>
        <div class="filter-group">
            <span class="filter-label">Assignee:</span>
            <button class="filter-btn active" onclick="setAssigneeFilter('all', this)">All</button>
            <button class="filter-btn" onclick="setAssigneeFilter('PES1UG24AM428', this)">Dharshini V</button>
            <button class="filter-btn" onclick="setAssigneeFilter('PES1UG24AM084', this)">Dhareen G</button>
            <button class="filter-btn" onclick="setAssigneeFilter('PES1UG24AM094', this)">Divyansh</button>
            <button class="filter-btn" onclick="setAssigneeFilter('PES1UG24AM087', this)">Dhruv Talavat</button>
        </div>
    </section>

    <!-- Main Container -->
    <main class="main-container">

        <!-- TAB 1: Active Sprint Board -->
        <div id="boardTab" class="tab-content active">
            <div class="board-grid">
                <!-- Column 1: Backlog / Committed -->
                <div class="board-column">
                    <div class="column-header">
                        <span>To Do</span>
                        <span class="column-counter" id="count-todo">0</span>
                    </div>
                    <div class="card-list" id="col-todo">
                        <div class="empty-column-placeholder">All sprint backlog items pulled into development.</div>
                    </div>
                </div>

                <!-- Column 2: In Progress -->
                <div class="board-column">
                    <div class="column-header">
                        <span>In Progress</span>
                        <span class="column-counter" id="count-inprogress">0</span>
                    </div>
                    <div class="card-list" id="col-inprogress">
                        <div class="empty-column-placeholder">No active tasks in progress (Sprint completed).</div>
                    </div>
                </div>

                <!-- Column 3: Code Review / PR -->
                <div class="board-column">
                    <div class="column-header">
                        <span>Code Review / PR</span>
                        <span class="column-counter" id="count-review">0</span>
                    </div>
                    <div class="card-list" id="col-review">
                        <div class="empty-column-placeholder">All pull requests reviewed and merged to main.</div>
                    </div>
                </div>

                <!-- Column 4: QA Testing & Verification -->
                <div class="board-column">
                    <div class="column-header">
                        <span>QA Testing</span>
                        <span class="column-counter" id="count-qa">0</span>
                    </div>
                    <div class="card-list" id="col-qa">
                        <div class="empty-column-placeholder">117 automated tests passing in CI/CD (100%).</div>
                    </div>
                </div>

                <!-- Column 5: Done / Accepted -->
                <div class="board-column">
                    <div class="column-header">
                        <span>Done (Accepted)</span>
                        <span class="column-counter" id="count-done">21</span>
                    </div>
                    <div class="card-list" id="col-done">
                        <!-- Populated by JS -->
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 2: Backlog & Sprints -->
        <div id="backlogTab" class="tab-content">

            <!-- Sprint 3 -->
            <div class="sprint-block">
                <div class="sprint-header">
                    <div class="sprint-title-area">
                        <span class="sprint-title">Sprint 3: Spill-Over Resolution, Fine Settlement & Test Reporting</span>
                        <span class="sprint-dates">2 Nov 2026 – 6 Nov 2026</span>
                    </div>
                    <div class="sprint-stats">
                        <span class="sprint-pill pill-sp">32 Story Points</span>
                        <span class="sprint-pill pill-done">Completed</span>
                    </div>
                </div>
                <table class="backlog-table">
                    <thead>
                        <tr>
                            <th style="width: 100px;">Key</th>
                            <th>Summary / User Story</th>
                            <th style="width: 180px;">Epic</th>
                            <th style="width: 160px;">Assignee</th>
                            <th style="width: 60px;">Points</th>
                            <th style="width: 90px;">Status</th>
                        </tr>
                    </thead>
                    <tbody id="sprint3-table-body"></tbody>
                </table>
            </div>

            <!-- Sprint 2 -->
            <div class="sprint-block">
                <div class="sprint-header">
                    <div class="sprint-title-area">
                        <span class="sprint-title">Sprint 2: Hold Lifecycle & Librarian Administration</span>
                        <span class="sprint-dates">26 Oct 2026 – 30 Oct 2026</span>
                    </div>
                    <div class="sprint-stats">
                        <span class="sprint-pill pill-sp">29 Story Points (5 Spill-over)</span>
                        <span class="sprint-pill pill-done">Completed</span>
                    </div>
                </div>
                <table class="backlog-table">
                    <thead>
                        <tr>
                            <th style="width: 100px;">Key</th>
                            <th>Summary / User Story</th>
                            <th style="width: 180px;">Epic</th>
                            <th style="width: 160px;">Assignee</th>
                            <th style="width: 60px;">Points</th>
                            <th style="width: 90px;">Status</th>
                        </tr>
                    </thead>
                    <tbody id="sprint2-table-body"></tbody>
                </table>
            </div>

            <!-- Sprint 1 -->
            <div class="sprint-block">
                <div class="sprint-header">
                    <div class="sprint-title-area">
                        <span class="sprint-title">Sprint 1: Core Search & Authentication Foundation</span>
                        <span class="sprint-dates">19 Oct 2026 – 23 Oct 2026</span>
                    </div>
                    <div class="sprint-stats">
                        <span class="sprint-pill pill-sp">24 Story Points</span>
                        <span class="sprint-pill pill-done">Completed</span>
                    </div>
                </div>
                <table class="backlog-table">
                    <thead>
                        <tr>
                            <th style="width: 100px;">Key</th>
                            <th>Summary / User Story</th>
                            <th style="width: 180px;">Epic</th>
                            <th style="width: 160px;">Assignee</th>
                            <th style="width: 60px;">Points</th>
                            <th style="width: 90px;">Status</th>
                        </tr>
                    </thead>
                    <tbody id="sprint1-table-body"></tbody>
                </table>
            </div>
        </div>

        <!-- TAB 3: Burndown Chart -->
        <div id="burndownTab" class="tab-content">
            <div class="burndown-card">
                <div class="burndown-title-row">
                    <div>
                        <h2>Sprint-3 Story Point Burndown Chart</h2>
                        <p style="color: var(--jira-subtle-text); font-size: 13px;">Committed: 32 Story Points | Completed: 32 Story Points (100% Velocity)</p>
                    </div>
                    <div>
                        <span class="meta-badge meta-badge-success">Burndown Reached 0 SP on Day 5</span>
                    </div>
                </div>

                <div class="burndown-chart-wrapper">
                    <svg class="chart-svg" viewBox="0 0 600 240">
                        <!-- Grid Lines -->
                        <line x1="50" y1="20" x2="550" y2="20" stroke="#ebecf0" stroke-width="1"/>
                        <line x1="50" y1="65" x2="550" y2="65" stroke="#ebecf0" stroke-width="1"/>
                        <line x1="50" y1="110" x2="550" y2="110" stroke="#ebecf0" stroke-width="1"/>
                        <line x1="50" y1="155" x2="550" y2="155" stroke="#ebecf0" stroke-width="1"/>
                        <line x1="50" y1="200" x2="550" y2="200" stroke="#dfe1e6" stroke-width="1.5"/>

                        <!-- Y-Axis Labels -->
                        <text x="25" y="25" class="chart-text">32 SP</text>
                        <text x="25" y="70" class="chart-text">24 SP</text>
                        <text x="25" y="115" class="chart-text">16 SP</text>
                        <text x="25" y="160" class="chart-text">8 SP</text>
                        <text x="25" y="205" class="chart-text">0 SP</text>

                        <!-- Ideal Burndown Line (Dashed) -->
                        <line x1="75" y1="20" x2="525" y2="200" class="chart-line-ideal"/>

                        <!-- Actual Burndown Line -->
                        <!-- Points: Day 1 (75, 20 [32]), Day 2 (187.5, 65 [24]), Day 3 (300, 155 [8]), Day 4 (412.5, 188.75 [2]), Day 5 (525, 200 [0]) -->
                        <polyline points="75,20 187.5,65 300,155 412.5,189 525,200" class="chart-line-actual"/>

                        <!-- Points -->
                        <circle cx="75" cy="20" r="5" class="chart-point"/>
                        <circle cx="187.5" cy="65" r="5" class="chart-point"/>
                        <circle cx="300" cy="155" r="5" class="chart-point"/>
                        <circle cx="412.5" cy="189" r="5" class="chart-point"/>
                        <circle cx="525" cy="200" r="5" class="chart-point"/>

                        <!-- Data Labels -->
                        <text x="75" y="12" class="chart-text" font-weight="bold" text-anchor="middle">32</text>
                        <text x="187.5" y="55" class="chart-text" font-weight="bold" text-anchor="middle">24</text>
                        <text x="300" y="145" class="chart-text" font-weight="bold" text-anchor="middle">8</text>
                        <text x="412.5" y="180" class="chart-text" font-weight="bold" text-anchor="middle">2</text>
                        <text x="525" y="192" class="chart-text" font-weight="bold" text-anchor="middle">0</text>

                        <!-- X-Axis Labels -->
                        <text x="75" y="222" class="chart-text" text-anchor="middle">Day 1 (Nov 2)</text>
                        <text x="187.5" y="222" class="chart-text" text-anchor="middle">Day 2 (Nov 3)</text>
                        <text x="300" y="222" class="chart-text" text-anchor="middle">Day 3 (Nov 4)</text>
                        <text x="412.5" y="222" class="chart-text" text-anchor="middle">Day 4 (Nov 5)</text>
                        <text x="525" y="222" class="chart-text" text-anchor="middle">Day 5 (Nov 6)</text>
                    </svg>
                </div>

                <h3 style="margin-top: 20px; font-size: 15px;">Daily Work Progression Log</h3>
                <table class="burndown-table">
                    <thead>
                        <tr>
                            <th>Date / Day</th>
                            <th>Starting SP</th>
                            <th>Issues Completed on Day</th>
                            <th>Remaining SP</th>
                            <th>Key Deliverables & Verification Highlights</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>Day 1 (Nov 2)</strong></td>
                            <td>32 SP</td>
                            <td>Sprint Planning & Architecture Alignment</td>
                            <td>32 SP</td>
                            <td>Groomed Sprint 3 backlog; incorporated 5 spill-over points; defined acceptance criteria.</td>
                        </tr>
                        <tr>
                            <td><strong>Day 2 (Nov 3)</strong></td>
                            <td>32 SP</td>
                            <td><code>LRG-301</code>, <code>LRG-304</code></td>
                            <td>24 SP</td>
                            <td>Overdue fine calculation module completed; 72-hour auto-expire cascade worker implemented.</td>
                        </tr>
                        <tr>
                            <td><strong>Day 3 (Nov 4)</strong></td>
                            <td>24 SP</td>
                            <td><code>LRG-302</code>, <code>LRG-303</code>, <code>LRG-306</code>, <code>LRG-307</code></td>
                            <td>8 SP</td>
                            <td>Campus Wallet / UPI payment settlement, fine hold restriction, sliding-window rate limiter, and GitHub Actions CI workflow completed.</td>
                        </tr>
                        <tr>
                            <td><strong>Day 4 (Nov 5)</strong></td>
                            <td>8 SP</td>
                            <td><code>LRG-305</code>, Unit Test Execution</td>
                            <td>2 SP</td>
                            <td>Notification retry engine completed; all 88 automated unit tests verified with 100% pass rate. Drafted Unit Test and System Validation reports.</td>
                        </tr>
                        <tr>
                            <td><strong>Day 5 (Nov 6)</strong></td>
                            <td>2 SP</td>
                            <td><code>LRG-308</code> (Full Test Reporting)</td>
                            <td><strong>0 SP</strong></td>
                            <td>Generated Code Coverage (89%) and Branch Coverage (82.6%) reports; final review and sign-off by all 4 team members.</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- TAB 4: Velocity & Epics -->
        <div id="velocityTab" class="tab-content">
            <div class="velocity-grid">
                <div class="velocity-card">
                    <div class="velocity-label">Total Story Points Delivered</div>
                    <div class="velocity-num">80 SP</div>
                    <p style="font-size: 12px; color: var(--jira-subtle-text);">Across 3 Sprints (24 + 24 + 32 completed)</p>
                </div>
                <div class="velocity-card">
                    <div class="velocity-label">Sprint 3 Velocity</div>
                    <div class="velocity-num">100%</div>
                    <p style="font-size: 12px; color: var(--jira-subtle-text);">32 points committed, 32 points closed</p>
                </div>
                <div class="velocity-card">
                    <div class="velocity-label">CI/CD Pass Rate</div>
                    <div class="velocity-num">100%</div>
                    <p style="font-size: 12px; color: var(--jira-subtle-text);">117 tests passing; zero open defects</p>
                </div>
            </div>

            <div class="burndown-card">
                <h3>Epics Completion Breakdown</h3>
                <table class="burndown-table" style="margin-top: 12px;">
                    <thead>
                        <tr>
                            <th>Epic ID</th>
                            <th>Epic Name</th>
                            <th>Owner</th>
                            <th>Story Points</th>
                            <th>SRS Requirements Covered</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>EPIC-1</strong></td>
                            <td>Catalog & Discovery Engine</td>
                            <td>Divyansh (PES1UG24AM094)</td>
                            <td>16 SP</td>
                            <td>LRG-F-001, LRG-F-002, LRG-NFR-001, UC-01, UC-02</td>
                            <td><span class="sprint-pill pill-done">100% Complete</span></td>
                        </tr>
                        <tr>
                            <td><strong>EPIC-2</strong></td>
                            <td>Member Circulation, Holds & Fines</td>
                            <td>Dharshini V (PES1UG24AM428)</td>
                            <td>32 SP</td>
                            <td>LRG-F-020 to 023, LRG-F-030 to 031, UC-03, UC-04, UC-04b</td>
                            <td><span class="sprint-pill pill-done">100% Complete</span></td>
                        </tr>
                        <tr>
                            <td><strong>EPIC-3</strong></td>
                            <td>Librarian Administration & Reporting</td>
                            <td>Dhareen G (PES1UG24AM084)</td>
                            <td>14 SP</td>
                            <td>LRG-F-040, LRG-F-041, UC-06, UC-08, UC-09</td>
                            <td><span class="sprint-pill pill-done">100% Complete</span></td>
                        </tr>
                        <tr>
                            <td><strong>EPIC-4</strong></td>
                            <td>Security Architecture, CI/CD & QA</td>
                            <td>Dhruv Talavat (PES1UG24AM087)</td>
                            <td>23 SP</td>
                            <td>LRG-SR-001 to 007, LRG-F-010, UC-05, All QA Reports</td>
                            <td><span class="sprint-pill pill-done">100% Complete</span></td>
                        </tr>
                    </tbody>
                </table>

                <h3 style="margin-top: 24px;">Team Capacity & Contribution Allocation</h3>
                <table class="burndown-table" style="margin-top: 12px;">
                    <thead>
                        <tr>
                            <th>Member Name</th>
                            <th>SRN</th>
                            <th>Primary Role</th>
                            <th>Assigned SP</th>
                            <th>Core Functional Subsystems</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>Dharshini V</strong></td>
                            <td><code>PES1UG24AM428</code></td>
                            <td>Dev Lead & Financial Subsystem Lead</td>
                            <td><strong>26 SP</strong></td>
                            <td>UC-04b Overdue Fine Settlement, Campus Wallet, Hold Gatekeeper, UI layout.</td>
                        </tr>
                        <tr>
                            <td><strong>Dhareen G</strong></td>
                            <td><code>PES1UG24AM084</code></td>
                            <td>QA Lead & Scrum Master</td>
                            <td><strong>21 SP</strong></td>
                            <td>SSO Auth engine, Title Return processing, Notification email queue, CI/CD pipeline, QA coordination.</td>
                        </tr>
                        <tr>
                            <td><strong>Dhruv Talavat</strong></td>
                            <td><code>PES1UG24AM087</code></td>
                            <td>Database & Security Lead</td>
                            <td><strong>21 SP</strong></td>
                            <td>SQLite ACID transactional schemas, FIFO queue re-sequencing, 72h auto-expire cascade, rate limiter.</td>
                        </tr>
                        <tr>
                            <td><strong>Divyansh</strong></td>
                            <td><code>PES1UG24AM094</code></td>
                            <td>Backend & Catalog Lead</td>
                            <td><strong>17 SP</strong></td>
                            <td>Catalog search index, input sanitization, hold cancellation, demand ranking analytics.</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- TAB 5: Traceability Matrix -->
        <div id="traceabilityTab" class="tab-content">
            <div class="burndown-card">
                <h2>SRS Requirements to Jira Traceability Matrix</h2>
                <p style="color: var(--jira-subtle-text); font-size: 13px; margin-bottom: 16px;">
                    Verifies full two-way traceability between submitted SRS requirements, Jira issue keys, and automated test cases.
                </p>
                <table class="burndown-table">
                    <thead>
                        <tr>
                            <th>SRS Req ID</th>
                            <th>Requirement Description</th>
                            <th>Use Case</th>
                            <th>Jira Issue Key</th>
                            <th>Module Source</th>
                            <th>Automated Test Case</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><code>LRG-F-001</code></td>
                            <td>Catalog search by Title, Author, ISBN</td>
                            <td>UC-01</td>
                            <td><code>LRG-102</code></td>
                            <td><code>src/catalog_search.py</code></td>
                            <td><code>TC-SRCH-01, 02, 07</code></td>
                        </tr>
                        <tr>
                            <td><code>LRG-F-002</code></td>
                            <td>Search input sanitization</td>
                            <td>UC-01</td>
                            <td><code>LRG-103</code></td>
                            <td><code>src/security.py</code></td>
                            <td><code>TC-SRCH-04, TC-SEC-02</code></td>
                        </tr>
                        <tr>
                            <td><code>LRG-F-010</code></td>
                            <td>Campus SSO authentication</td>
                            <td>UC-05</td>
                            <td><code>LRG-104</code></td>
                            <td><code>src/auth.py</code></td>
                            <td><code>TC-AUTH-01, 02, 03</code></td>
                        </tr>
                        <tr>
                            <td><code>LRG-F-020</code></td>
                            <td>Place hold on Checked-Out title</td>
                            <td>UC-03</td>
                            <td><code>LRG-201</code></td>
                            <td><code>src/reservation_manager.py</code></td>
                            <td><code>TC-HOLD-01</code></td>
                        </tr>
                        <tr>
                            <td><code>LRG-F-021</code></td>
                            <td>Prevent duplicate & available holds</td>
                            <td>UC-03</td>
                            <td><code>LRG-202</code></td>
                            <td><code>src/reservation_manager.py</code></td>
                            <td><code>TC-HOLD-02, 03</code></td>
                        </tr>
                        <tr>
                            <td><code>LRG-F-022</code></td>
                            <td>View and cancel active hold</td>
                            <td>UC-04</td>
                            <td><code>LRG-203</code></td>
                            <td><code>src/reservation_manager.py</code></td>
                            <td><code>TC-HOLD-04</code></td>
                        </tr>
                        <tr>
                            <td><code>LRG-F-023</code></td>
                            <td>FIFO queue position progression</td>
                            <td>UC-03</td>
                            <td><code>LRG-204</code></td>
                            <td><code>src/reservation_manager.py</code></td>
                            <td><code>TC-HOLD-05</code></td>
                        </tr>
                        <tr>
                            <td><code>LRG-F-030</code></td>
                            <td>Overdue fine balance computation</td>
                            <td>UC-04b</td>
                            <td><code>LRG-301</code></td>
                            <td><code>src/fine_manager.py</code></td>
                            <td><code>TC-FINE-01</code></td>
                        </tr>
                        <tr>
                            <td><code>LRG-F-031</code></td>
                            <td>Campus Wallet / UPI settlement</td>
                            <td>UC-04b</td>
                            <td><code>LRG-302</code></td>
                            <td><code>src/fine_manager.py</code></td>
                            <td><code>TC-FINE-02, 03</code></td>
                        </tr>
                        <tr>
                            <td><code>LRG-F-040</code></td>
                            <td>Title return & hold promotion</td>
                            <td>UC-06</td>
                            <td><code>LRG-205</code></td>
                            <td><code>src/admin.py</code></td>
                            <td><code>TC-ADM-01</code></td>
                        </tr>
                        <tr>
                            <td><code>LRG-F-041</code></td>
                            <td>Hold demand ranking report</td>
                            <td>UC-09</td>
                            <td><code>LRG-206</code></td>
                            <td><code>src/admin.py</code></td>
                            <td><code>TC-ADM-02</code></td>
                        </tr>
                        <tr>
                            <td><code>LRG-SR-005</code></td>
                            <td>Brute force login lockout (5 attempts)</td>
                            <td>UC-05</td>
                            <td><code>LRG-104</code></td>
                            <td><code>src/auth.py</code></td>
                            <td><code>TC-AUTH-03</code></td>
                        </tr>
                        <tr>
                            <td><code>LRG-SR-007</code></td>
                            <td>Sliding-window rate limiter (60/min)</td>
                            <td>All</td>
                            <td><code>LRG-306</code></td>
                            <td><code>src/security.py</code></td>
                            <td><code>TC-SEC-07</code></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

    </main>

    <!-- Issue Detail Modal -->
    <div id="issueModal" class="jira-modal-backdrop" onclick="closeModalOnBackdrop(event)">
        <div class="jira-modal">
            <div class="modal-header">
                <div>
                    <span id="modalIssueKey" class="card-key" style="font-size: 14px;">LRG-301</span>
                    <span id="modalEpicTag" class="card-epic-tag epic-fines" style="margin-left: 8px;">EPIC-2: Member Circulation & Fines</span>
                </div>
                <button class="modal-close-btn" onclick="closeModal()">X</button>
            </div>
            <div class="modal-body">
                <div class="modal-left">
                    <h3 id="modalSummary">Summary</h3>
                    
                    <div class="modal-section-title">Description</div>
                    <div id="modalDesc" class="modal-desc-box"></div>

                    <div class="modal-section-title">Acceptance Criteria</div>
                    <div id="modalAC" class="modal-desc-box"></div>

                    <div class="modal-section-title">Definition of Done (DoD)</div>
                    <div id="modalDoD" class="modal-desc-box"></div>

                    <div class="modal-section-title">Quality Assurance & Verification</div>
                    <div id="modalQA" class="modal-desc-box"></div>
                </div>
                <div class="modal-right">
                    <div class="modal-attr-group">
                        <div class="attr-label">Status</div>
                        <div class="attr-value"><span class="sprint-pill pill-done">DONE</span></div>
                    </div>
                    <div class="modal-attr-group">
                        <div class="attr-label">Resolution</div>
                        <div class="attr-value">Done / Fixed</div>
                    </div>
                    <div class="modal-attr-group">
                        <div class="attr-label">Assignee</div>
                        <div id="modalAssignee" class="attr-value">Dharshini V</div>
                    </div>
                    <div class="modal-attr-group">
                        <div class="attr-label">SRN</div>
                        <div id="modalSRN" class="attr-value"><code>PES1UG24AM428</code></div>
                    </div>
                    <div class="modal-attr-group">
                        <div class="attr-label">Story Points</div>
                        <div id="modalPoints" class="attr-value">5 (Fibonacci)</div>
                    </div>
                    <div class="modal-attr-group">
                        <div class="attr-label">Sprint</div>
                        <div id="modalSprint" class="attr-value">Sprint 3</div>
                    </div>
                    <div class="modal-attr-group">
                        <div class="attr-label">Priority</div>
                        <div id="modalPriority" class="attr-value">Highest</div>
                    </div>
                    <div class="modal-attr-group">
                        <div class="attr-label">Pull Request</div>
                        <div id="modalPR" class="attr-value">Merged to <code>main</code></div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Jira Issue Data and Client Scripts -->
    <script>
        const JIRA_ISSUES = [
            // Sprint 1
            {
                key: "LRG-101",
                sprint: "sprint-1",
                summary: "Relational SQLite Schema & Initial Seed Data",
                assigneeName: "Dhruv Talavat",
                assigneeSRN: "PES1UG24AM087",
                avatar: "dt",
                points: 5,
                epic: "EPIC-4: Infrastructure & Security",
                epicClass: "epic-sec",
                priority: "Highest",
                desc: "Design and deploy the relational SQLite database with foreign key cascades, unique constraints, and initial test catalog.",
                ac: "Given a fresh environment, running schema creation provisions titles, members, holds, fines, and audit_log tables with zero foreign-key errors.",
                dod: "Database initialization script runs deterministically in CI; migration logic supports forward-compatible column additions.",
                qa: "Verified in test_database.py and conftest.py fixtures."
            },
            {
                key: "LRG-102",
                sprint: "sprint-1",
                summary: "Catalog Search by Title, Author, ISBN (LRG-F-001)",
                assigneeName: "Divyansh",
                assigneeSRN: "PES1UG24AM094",
                avatar: "dy",
                points: 5,
                epic: "EPIC-1: Catalog & Discovery",
                epicClass: "epic-catalog",
                priority: "Highest",
                desc: "Implement high-speed indexed search across 100,000+ catalog titles supporting ISBN-10, ISBN-13, partial title, and author matching.",
                ac: "Sub-second response time for search queries; normalized ISBN matches regardless of hyphens.",
                dod: "Search service handles exact and partial string queries; tested across 120 seed titles with pagination.",
                qa: "Verified in TC-SRCH-01, TC-SRCH-02, TC-SRCH-07 in test_catalog_search.py."
            },
            {
                key: "LRG-103",
                sprint: "sprint-1",
                summary: "Search Input Validation & Sanitization (LRG-F-002)",
                assigneeName: "Divyansh",
                assigneeSRN: "PES1UG24AM094",
                avatar: "dy",
                points: 3,
                epic: "EPIC-1: Catalog & Discovery",
                epicClass: "epic-catalog",
                priority: "High",
                desc: "Sanitize all user search inputs to neutralize SQL injection vectors and cross-site scripting (XSS) payloads.",
                ac: "SQL wildcards, HTML tags, and null bytes are escaped; empty or whitespace-only queries prompt the user without crashing.",
                dod: "Parameterized SQL queries exclusively used; passed all OWASP benchmark tests.",
                qa: "Verified in TC-SRCH-04 and TC-SEC-02 in test_security_audit.py."
            },
            {
                key: "LRG-104",
                sprint: "sprint-1",
                summary: "Campus SSO Authentication & Session Engine (LRG-F-010)",
                assigneeName: "Dhareen G",
                assigneeSRN: "PES1UG24AM084",
                avatar: "dg",
                points: 5,
                epic: "EPIC-4: Infrastructure & Security",
                epicClass: "epic-sec",
                priority: "Highest",
                desc: "OpenID Connect SSO token verification, RBAC role assignment (student vs librarian), 30-min idle session timeout, and 5-attempt brute-force lockout.",
                ac: "Valid SSO token establishes session; 5 consecutive failed attempts lock account for 15 minutes.",
                dod: "Passes timing attacks; audit logs record authentication failures; session cookie sets HttpOnly and SameSite=Strict.",
                qa: "Verified in TC-AUTH-01, TC-AUTH-02, TC-AUTH-03 in test_auth.py."
            },
            {
                key: "LRG-105",
                sprint: "sprint-1",
                summary: "Responsive Catalog Search Web UI",
                assigneeName: "Dharshini V",
                assigneeSRN: "PES1UG24AM428",
                avatar: "dv",
                points: 3,
                epic: "EPIC-1: Catalog & Discovery",
                epicClass: "epic-catalog",
                priority: "Medium",
                desc: "Mobile-responsive web interface meeting WCAG 2.1 AA standards for catalog searching, pagination, and book cards.",
                ac: "UI renders properly from 360px viewport width up; color contrast >= 4.5:1; fully keyboard navigable.",
                dod: "Validated across desktop and mobile breakpoints; passes HTML5 semantic validation.",
                qa: "Verified in TC-UX-01 in test_system_e2e.py."
            },
            {
                key: "LRG-106",
                sprint: "sprint-1",
                summary: "Baseline Unit Tests for Search & Authentication",
                assigneeName: "Dhareen G",
                assigneeSRN: "PES1UG24AM084",
                avatar: "dg",
                points: 3,
                epic: "EPIC-4: Infrastructure & Security",
                epicClass: "epic-sec",
                priority: "Medium",
                desc: "Establish hermetic test suite for Sprint 1 deliverables with automated pytest execution and fixture setup.",
                ac: "All 18 initial unit tests pass without network dependencies in under 2 seconds.",
                dod: "Test runner integrated into makefile/scripts; zero flaky tests.",
                qa: "Verified via pytest run producing 100% pass rate."
            },

            // Sprint 2
            {
                key: "LRG-201",
                sprint: "sprint-2",
                summary: "Place Hold on Checked-Out Book (LRG-F-020)",
                assigneeName: "Dharshini V",
                assigneeSRN: "PES1UG24AM428",
                avatar: "dv",
                points: 5,
                epic: "EPIC-2: Member Circulation & Fines",
                epicClass: "epic-fines",
                priority: "Highest",
                desc: "Allow authenticated students to place reservation holds on checked-out titles with automated FIFO queue position assignment.",
                ac: "Hold request successfully allocates next available sequential position in queue.",
                dod: "ACID transaction guarantees queue consistency under concurrent hold requests.",
                qa: "Verified in TC-HOLD-01 in test_reservation_manager.py."
            },
            {
                key: "LRG-202",
                sprint: "sprint-2",
                summary: "Prevent Duplicate & Available Holds (LRG-F-021)",
                assigneeName: "Dharshini V",
                assigneeSRN: "PES1UG24AM428",
                avatar: "dv",
                points: 3,
                epic: "EPIC-2: Member Circulation & Fines",
                epicClass: "epic-fines",
                priority: "High",
                desc: "Enforce business validation rules: reject holds if the book is currently Available, or if the student already has an active hold.",
                ac: "User receives clear explanatory error message; database state remains unchanged.",
                dod: "Validation occurs before transaction commit; distinct HTTP error codes returned.",
                qa: "Verified in TC-HOLD-02, TC-HOLD-03 in test_reservation_manager.py."
            },
            {
                key: "LRG-203",
                sprint: "sprint-2",
                summary: "View & Cancel Active Holds (LRG-F-022)",
                assigneeName: "Divyansh",
                assigneeSRN: "PES1UG24AM094",
                avatar: "dy",
                points: 3,
                epic: "EPIC-2: Member Circulation & Fines",
                epicClass: "epic-fines",
                priority: "High",
                desc: "Provide student portal view of active holds with instant cancellation and authorization check.",
                ac: "Students can only cancel their own holds; unauthorized cancel attempts return 403 Forbidden.",
                dod: "Queue positions of subsequent members automatically shift up by 1.",
                qa: "Verified in TC-HOLD-04 in test_reservation_manager.py."
            },
            {
                key: "LRG-204",
                sprint: "sprint-2",
                summary: "Dynamic FIFO Queue Position Progression (LRG-F-023)",
                assigneeName: "Dhruv Talavat",
                assigneeSRN: "PES1UG24AM087",
                avatar: "dt",
                points: 5,
                epic: "EPIC-2: Member Circulation & Fines",
                epicClass: "epic-fines",
                priority: "High",
                desc: "Automate queue re-sequencing upon cancellation or fulfillment so queue positions remain gapless.",
                ac: "Position 1 member promoted to Ready; position 2 shifts to 1, position 3 shifts to 2.",
                dod: "Database updates wrapped in BEGIN IMMEDIATE transaction to prevent deadlocks.",
                qa: "Verified in TC-HOLD-05 in test_reservation_manager.py."
            },
            {
                key: "LRG-205",
                sprint: "sprint-2",
                summary: "Return Title & Hold Promotion to Ready (LRG-F-040)",
                assigneeName: "Dhareen G",
                assigneeSRN: "PES1UG24AM084",
                avatar: "dg",
                points: 5,
                epic: "EPIC-3: Librarian Admin & Reporting",
                epicClass: "epic-admin",
                priority: "Highest",
                desc: "Librarian dashboard endpoint to mark returned books, check for pending holds, and promote position-1 to Ready status.",
                ac: "Book marked Reserved for pickup; Ready status timestamp recorded; pickup window set to 72 hours.",
                dod: "If no holds exist, book status resets to Available; audit log records return event.",
                qa: "Verified in TC-ADM-01 in test_admin.py."
            },
            {
                key: "LRG-206",
                sprint: "sprint-2",
                summary: "Hold Demand Report for Librarian (LRG-F-041)",
                assigneeName: "Divyansh",
                assigneeSRN: "PES1UG24AM094",
                avatar: "dy",
                points: 3,
                epic: "EPIC-3: Librarian Admin & Reporting",
                epicClass: "epic-admin",
                priority: "Medium",
                desc: "Generate aggregated report of high-demand titles ranked by queue length to inform procurement decisions.",
                ac: "Returns list of titles with >= 1 hold, sorted descending by active hold count.",
                dod: "Restricted to librarian role; accessible via Web UI and JSON API.",
                qa: "Verified in TC-ADM-02 in test_admin.py."
            },

            // Sprint 3
            {
                key: "LRG-301",
                sprint: "sprint-3",
                summary: "UC-04: Overdue Fine Assessment & Balance Engine",
                assigneeName: "Dharshini V",
                assigneeSRN: "PES1UG24AM428",
                avatar: "dv",
                points: 5,
                epic: "EPIC-2: Member Circulation & Fines",
                epicClass: "epic-fines",
                priority: "Highest",
                desc: "Calculate daily late fees at $1/day from due date; track itemized fine records per student in relational table.",
                ac: "Accurate calendar-day fine calculation; unpaid balance reflected immediately on student portal.",
                dod: "Zero negative fine amounts permitted; handles edge cases of same-day and multi-week overdue titles.",
                qa: "Verified in TC-FINE-01 in test_fine_manager.py."
            },
            {
                key: "LRG-302",
                sprint: "sprint-3",
                summary: "UC-04: Campus Wallet / UPI Settlement & Digital Receipt",
                assigneeName: "Dharshini V",
                assigneeSRN: "PES1UG24AM428",
                avatar: "dv",
                points: 5,
                epic: "EPIC-2: Member Circulation & Fines",
                epicClass: "epic-fines",
                priority: "Highest",
                desc: "Process fine payments via simulated Campus Wallet or UPI; issue cryptographically verifiable digital receipts.",
                ac: "Fine marked PAID with transaction timestamp; balance resets to $0.00; receipt issuance logged in audit table.",
                dod: "Atomic settlement; students can view and download transaction receipts.",
                qa: "Verified in TC-FINE-02 in test_fine_manager.py."
            },
            {
                key: "LRG-303",
                sprint: "sprint-3",
                summary: "UC-04: Hold Restriction when Unpaid Fines >= $20",
                assigneeName: "Dharshini V",
                assigneeSRN: "PES1UG24AM428",
                avatar: "dv",
                points: 3,
                epic: "EPIC-2: Member Circulation & Fines",
                epicClass: "epic-fines",
                priority: "High",
                desc: "Prevent members with overdue fines >= $20 from placing new holds until dues are settled.",
                ac: "Hold placement returns 403 Forbidden with prompt to clear outstanding dues; holds allowed immediately once cleared.",
                dod: "Check performed at service layer before queue entry; clear user guidance displayed in UI.",
                qa: "Verified in TC-FINE-03 in test_fine_manager.py."
            },
            {
                key: "LRG-304",
                sprint: "sprint-3",
                summary: "72-Hour Ready Hold Auto-Expiration & Cascade Promotion",
                assigneeName: "Dhruv Talavat",
                assigneeSRN: "PES1UG24AM087",
                avatar: "dt",
                points: 5,
                epic: "EPIC-2: Member Circulation & Fines",
                epicClass: "epic-fines",
                priority: "Highest",
                desc: "Spill-Over 1: Automated worker that expires unclaimed Ready holds after 72 hours and cascades hold-ready status to next member.",
                ac: "Expired hold marked Cancelled; position-2 promoted to Ready; pickup window reset to 72 hours; email dispatched.",
                dod: "Runs on schedule or trigger; handles empty queue by returning book to Available status.",
                qa: "Verified in TC-HOLD-06 in test_reservation_manager.py."
            },
            {
                key: "LRG-305",
                sprint: "sprint-3",
                summary: "Notification Retry Engine & Failure Audit Logging",
                assigneeName: "Divyansh",
                assigneeSRN: "PES1UG24AM094",
                avatar: "dy",
                points: 3,
                epic: "EPIC-2: Member Circulation & Fines",
                epicClass: "epic-fines",
                priority: "Medium",
                desc: "Spill-Over 2: Implement exponential backoff retry queue (3 attempts) on SMTP dispatch failure with dead-letter logging.",
                ac: "Transient failures retried automatically; permanent failures written to audit log with error details.",
                dod: "Zero uncaught socket exceptions bubble up to user thread; notification log tracks dispatch attempts.",
                qa: "Verified in TC-NOTF-03 in test_notification.py."
            },
            {
                key: "LRG-306",
                sprint: "sprint-3",
                summary: "Sliding-Window Rate Limiter & Cookie Security (LRG-SR-007)",
                assigneeName: "Dhruv Talavat",
                assigneeSRN: "PES1UG24AM087",
                avatar: "dt",
                points: 3,
                epic: "EPIC-4: Infrastructure & Security",
                epicClass: "epic-sec",
                priority: "High",
                desc: "Spill-Over 3: In-memory sliding-window rate limiter (60 req/min/IP) and security cookie attributes (HttpOnly, SameSite=Strict).",
                ac: "Exceeding 60 req/min returns HTTP 429 Too Many Requests with Retry-After header.",
                dod: "Cookie flags verified by automated headers inspection; rate limiter thread-safe.",
                qa: "Verified in TC-SEC-03, TC-SEC-07 in test_security_audit.py."
            },
            {
                key: "LRG-307",
                sprint: "sprint-3",
                summary: "Automated GitHub Actions CI/CD Pipeline (ci.yml)",
                assigneeName: "Dhareen G",
                assigneeSRN: "PES1UG24AM084",
                avatar: "dg",
                points: 3,
                epic: "EPIC-4: Infrastructure & Security",
                epicClass: "epic-sec",
                priority: "High",
                desc: "Continuous integration pipeline executing environment setup, flake8 linting, hermetic pytest runs, and 70% coverage gating.",
                ac: "Workflow triggers on push and pull-request; fails build if coverage < 70% or any test fails.",
                dod: "Artifact archiving saves coverage HTML/XML reports for 30 days.",
                qa: "Verified via GitHub Actions workflow run logs."
            },
            {
                key: "LRG-308",
                sprint: "sprint-3",
                summary: "Execute Full Test Plan & Generate 4 Mandatory Test Reports",
                assigneeName: "Dhareen G & Dharshini V",
                assigneeSRN: "PES1UG24AM084 / PES1UG24AM428",
                avatar: "dg",
                points: 5,
                epic: "EPIC-4: Infrastructure & Security",
                epicClass: "epic-sec",
                priority: "Highest",
                desc: "Execute complete test plan and compile Unit Test Report, System Validation Report, Code Coverage Report, and Branch Coverage Report.",
                ac: "Four comprehensive markdown reports authored, signed off, and uploaded to docs/ in project repository.",
                dod: "100% test pass rate (88/88 tests initially, 117/117 expanded); >= 70% code coverage achieved.",
                qa: "Verified via docs/ reports and pytest-cov outputs."
            }
        ];

        let currentSprintFilter = 'all';
        let currentAssigneeFilter = 'all';
        let currentSearchQuery = '';

        function renderBoard() {
            const colDone = document.getElementById('col-done');
            colDone.innerHTML = '';

            const filtered = JIRA_ISSUES.filter(issue => {
                const matchSprint = (currentSprintFilter === 'all') || (issue.sprint === currentSprintFilter);
                const matchAssignee = (currentAssigneeFilter === 'all') || (issue.assigneeSRN === currentAssigneeFilter);
                const matchSearch = (currentSearchQuery === '') ||
                    issue.key.toLowerCase().includes(currentSearchQuery) ||
                    issue.summary.toLowerCase().includes(currentSearchQuery) ||
                    issue.assigneeName.toLowerCase().includes(currentSearchQuery);
                return matchSprint && matchAssignee && matchSearch;
            });

            document.getElementById('count-done').innerText = filtered.length;

            filtered.forEach(issue => {
                const card = document.createElement('div');
                card.className = 'jira-card';
                card.onclick = () => openModal(issue.key);

                card.innerHTML = `
                    <span class="card-epic-tag ${issue.epicClass}">${issue.epic.split(':')[0]}</span>
                    <div class="card-summary">${issue.summary}</div>
                    <div class="card-meta">
                        <div class="card-meta-left">
                            <span class="issue-type-tag">Story</span>
                            <span class="card-key">${issue.key}</span>
                        </div>
                        <div class="card-meta-right">
                            <span class="sp-badge" title="Story Points">${issue.points}</span>
                            <div class="assignee-avatar avatar-${issue.avatar}" title="${issue.assigneeName} (${issue.assigneeSRN})">
                                ${issue.assigneeName.split(' ').map(n=>n[0]).join('')}
                            </div>
                        </div>
                    </div>
                `;
                colDone.appendChild(card);
            });
        }

        function renderBacklogTables() {
            const s3 = JIRA_ISSUES.filter(i => i.sprint === 'sprint-3');
            const s2 = JIRA_ISSUES.filter(i => i.sprint === 'sprint-2');
            const s1 = JIRA_ISSUES.filter(i => i.sprint === 'sprint-1');

            populateTable('sprint3-table-body', s3);
            populateTable('sprint2-table-body', s2);
            populateTable('sprint1-table-body', s1);
        }

        function populateTable(elementId, issues) {
            const tbody = document.getElementById(elementId);
            tbody.innerHTML = '';
            issues.forEach(issue => {
                const tr = document.createElement('tr');
                tr.onclick = () => openModal(issue.key);
                tr.innerHTML = `
                    <td><strong class="card-key">${issue.key}</strong></td>
                    <td>${issue.summary}</td>
                    <td><span class="card-epic-tag ${issue.epicClass}">${issue.epic}</span></td>
                    <td>${issue.assigneeName}</td>
                    <td><span class="sp-badge">${issue.points}</span></td>
                    <td><span class="sprint-pill pill-done">DONE</span></td>
                `;
                tbody.appendChild(tr);
            });
        }

        function switchTab(tabId, el) {
            document.querySelectorAll('.tab-content').forEach(tc => tc.classList.remove('active'));
            document.querySelectorAll('.jira-tab').forEach(t => t.classList.remove('active'));

            document.getElementById(tabId).classList.add('active');
            el.classList.add('active');
        }

        function setSprintFilter(sprint, el) {
            currentSprintFilter = sprint;
            el.parentElement.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            el.classList.add('active');
            renderBoard();
        }

        function setAssigneeFilter(srn, el) {
            currentAssigneeFilter = srn;
            el.parentElement.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            el.classList.add('active');
            renderBoard();
        }

        function filterBySearch() {
            currentSearchQuery = document.getElementById('searchInput').value.trim().toLowerCase();
            renderBoard();
        }

        function openModal(key) {
            const issue = JIRA_ISSUES.find(i => i.key === key);
            if (!issue) return;

            document.getElementById('modalIssueKey').innerText = issue.key;
            document.getElementById('modalSummary').innerText = issue.summary;
            document.getElementById('modalEpicTag').innerText = issue.epic;
            document.getElementById('modalEpicTag').className = `card-epic-tag ${issue.epicClass}`;
            document.getElementById('modalDesc').innerText = issue.desc;
            document.getElementById('modalAC').innerText = issue.ac;
            document.getElementById('modalDoD').innerText = issue.dod;
            document.getElementById('modalQA').innerText = issue.qa;

            document.getElementById('modalAssignee').innerText = issue.assigneeName;
            document.getElementById('modalSRN').innerHTML = `<code>${issue.assigneeSRN}</code>`;
            document.getElementById('modalPoints').innerText = `${issue.points} Story Points`;
            document.getElementById('modalSprint').innerText = issue.sprint.toUpperCase().replace('-', ' ');
            document.getElementById('modalPriority').innerText = issue.priority;

            document.getElementById('issueModal').style.display = 'flex';
        }

        function closeModal() {
            document.getElementById('issueModal').style.display = 'none';
        }

        function closeModalOnBackdrop(e) {
            if (e.target.id === 'issueModal') {
                closeModal();
            }
        }

        // Initialize on load
        window.onload = function() {
            renderBoard();
            renderBacklogTables();
        };
    </script>
</body>
</html>
"""

output_path = r"C:\Users\Dharshini\.gemini\antigravity\scratch\SE-Lab-Project-PES1UG24AM084-PES1UG24AM428-PES1UG24AM094-PES1UG24AM087\docs\jira_dashboard.html"

with open(output_path, "w", encoding="utf-8") as f:
    f.write(HTML_CONTENT)

print(f"Jira Dashboard successfully generated at: {output_path}")
print(f"File size: {os.path.getsize(output_path)} bytes")
