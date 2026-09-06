-- ============================================================
-- 大A舆情预判框架 - SQLite数据库骨架
-- 创建日期: 2026-09-03
-- 版本: v2.0 (P0改造后，基于10位专家评审)
-- 设计原则:
--   1. SQLite存结构化/时序数据，Obsidian存人类可读报告
--   2. 所有数据带可用时间戳(available_at)，防止前视偏差
--   3. 稳健z-score用中位数+MAD，非普通z-score
--   4. 支持信号衰减追踪和熔断机制
-- ============================================================

PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

-- ============================================================
-- 1. market_snapshot - 每日市场快照（综合情绪评分）
-- ============================================================
CREATE TABLE IF NOT EXISTS market_snapshot (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trade_date TEXT NOT NULL,              -- 交易日 YYYY-MM-DD
    available_at TEXT NOT NULL,            -- 数据可用时间 ISO-8601（防前视偏差）

    -- L0 宏观周期层 (30%)
    l0_social_finance_z REAL,              -- 社融存量同比 z-score
    l0_m1_m2_scissors_z REAL,              -- M1-M2剪刀差 z-score
    l0_pmi_z REAL,                         -- PMI z-score
    l0_credit_structure_z REAL,            -- 中长贷占比 z-score
    l0_dr007_z REAL,                        -- DR007 z-score
    l0_cpi_ppi_z REAL,                     -- CPI-PPI剪刀差 z-score
    l0_macro_score REAL,                   -- L0综合得分

    -- L1 政策与监管层 (15%)
    l1_policy_event_count INTEGER,         -- 政策事件数
    l1_policy_strength REAL,               -- 政策力度分级(1-5)
    l1_policy_direction TEXT,              -- 'bullish'/'bearish'/'neutral'
    l1_policy_score REAL,                  -- L1综合得分

    -- L2 机构动向层 (20%)
    l2_lhb_inst_net_buy REAL,             -- 龙虎榜机构净买入(亿)
    l2_lhb_retail_net_buy REAL,            -- 龙虎榜游资净买入(亿)
    l2_lhb_divergence REAL,                -- 机构vs游资分歧度
    l2_margin_balance_change REAL,         -- 融资融券余额变化(亿)
    l2_block_trade_discount REAL,          -- 大宗交易折价率
    l2_inst_score REAL,                    -- L2综合得分

    -- L3 资金面层 (20%)
    l3_northbound_net REAL,                -- 北向资金净流入(亿) - 降权后
    l3_main_capital_net REAL,              -- 主力资金净流入(亿)
    l3_auction_anomaly REAL,              -- 竞价异动信号强度
    l3_etf_net_subscribe REAL,             -- ETF净申赎(亿)
    l3_cds_spread REAL,                    -- CDS利差/信用利差
    l3_capital_score REAL,                 -- L3综合得分

    -- L4 市场情绪层 (15%)
    l4_limit_up_count INTEGER,             -- 涨停数
    l4_broken_limit_count INTEGER,         -- 炸板数
    l4_broken_rate REAL,                   -- 炸板率
    l4_consecutive_max INTEGER,            -- 连板最高板数
    l4_consecutive_success_rate REAL,      -- 连板晋级率(二进三成功率)
    l4_board_rotation_speed REAL,          -- 板块轮动速度
    l4_turnover_ratio REAL,               -- 换手率分位数
    l4_volume_ratio REAL,                  -- 成交额/20日均值
    l4_sentiment_score REAL,              -- L4综合得分

    -- L5 衍生品层 (15%) - 新增
    l5_pcr_position REAL,                  -- 持仓量PCR
    l5_iv_change REAL,                      -- IV变化率
    l5_iv_term_structure REAL,             -- IV期限结构(近月-远月)
    l5_basis_if REAL,                       -- IF基差
    l5_basis_ic REAL,                       -- IC基差
    l5_skew_25delta REAL,                  -- 25Delta Skew
    l5_derivatives_score REAL,             -- L5综合得分

    -- 舆情极端值预警 (不纳入权重，仅极端值触发)
    sentiment_extreme_flag TEXT,           -- 'overheat'/'panic'/NULL

    -- 综合评分
    composite_score REAL,                  -- 综合稳健z-score
    composite_percentile REAL,             -- 综合历史分位数(0-1)
    composite_direction TEXT,              -- 'bullish'/'bearish'/'neutral'
    composite_confidence REAL,             -- 置信度(0-1)

    -- 熔断状态
    circuit_breaker_level INTEGER DEFAULT 0,  -- 0=正常,1=降权,2=暂停,3=冻结
    circuit_breaker_reason TEXT,               -- 触发原因

    -- 元数据
    created_at TEXT DEFAULT (datetime('now', '+8 hours')),
    updated_at TEXT DEFAULT (datetime('now', '+8 hours')),

    UNIQUE(trade_date)
);

-- ============================================================
-- 2. capital_flow - 资金流明细（日频）
-- ============================================================
CREATE TABLE IF NOT EXISTS capital_flow (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trade_date TEXT NOT NULL,
    available_at TEXT NOT NULL,

    -- 北向资金
    northbound_sh_net REAL,                -- 沪股通净流入(亿)
    northbound_sz_net REAL,                -- 深股通净流入(亿)
    northbound_total_net REAL,             -- 北向合计净流入(亿)
    northbound_5d_avg REAL,                -- 5日滚动均值

    -- 主力资金
    main_capital_net REAL,                 -- 主力净流入(亿)
    main_capital_large_order REAL,         -- 大单净流入
    main_capital_small_order REAL,         -- 小单净流入

    -- 融资融券
    margin_balance REAL,                  -- 融资余额(亿)
    margin_buy_value REAL,                -- 融资买入额(亿)
    margin_buy_ratio REAL,                -- 融资买入/总成交额
    short_balance REAL,                    -- 融券余额(亿)

    -- ETF资金
    etf_net_subscribe REAL,               -- ETF净申赎(亿)
    broad_etf_net REAL,                   -- 宽基ETF净申赎
    sector_etf_net REAL,                  -- 行业ETF净申赎

    -- 公募基金（周频/季频，NULL=未更新）
    public_fund_position REAL,            -- 公募股票仓位(%)
    public_fund_position_change REAL,     -- 仓位变化

    created_at TEXT DEFAULT (datetime('now', '+8 hours')),
    UNIQUE(trade_date)
);

-- ============================================================
-- 3. limit_up_pool - 涨停池/炸板/连板数据
-- ============================================================
CREATE TABLE IF NOT EXISTS limit_up_pool (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trade_date TEXT NOT NULL,
    available_at TEXT NOT NULL,

    -- 涨停池
    limit_up_count INTEGER,               -- 涨停家数
    limit_up_first_board INTEGER,          -- 首板数
    limit_up_second_board INTEGER,        -- 二板数
    limit_up_third_plus INTEGER,          -- 三板及以上数
    limit_up_one_word INTEGER,            -- 一字板数
    limit_up_turnover_board INTEGER,      -- 换手板数

    -- 炸板
    broken_limit_count INTEGER,           -- 炸板家数
    broken_rate REAL,                     -- 炸板率
    two_to_three_success_rate REAL,       -- 二进三成功率
    three_to_four_success_rate REAL,      -- 三进四成功率

    -- 连板天梯
    max_consecutive_boards INTEGER,        -- 最高连板数
    consecutive_ladder TEXT,              -- 连板天梯JSON: {板数:家数}

    -- 板块集中度
    top_sector_concentration REAL,        -- 前三板块涨停占比
    sector_distribution TEXT,             -- 板块分布JSON

    -- 赚钱效应
    yesterday_limit_up_today_avg REAL,   -- 昨日涨停今日均涨幅
    making_money_index REAL,              -- 赚钱效应指数

    created_at TEXT DEFAULT (datetime('now', '+8 hours')),
    UNIQUE(trade_date)
);

-- ============================================================
-- 4. macro_indicators - 宏观经济指标（月频/日频混合）
-- ============================================================
CREATE TABLE IF NOT EXISTS macro_indicators (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    indicator_date TEXT NOT NULL,          -- 指标日期
    available_at TEXT NOT NULL,            -- 数据发布日期(防前视偏差)
    indicator_name TEXT NOT NULL,          -- 指标名称
    indicator_value REAL,                  -- 指标值
    indicator_unit TEXT,                   -- 单位
    expected_value REAL,                   -- 市场一致预期
    surprise REAL,                         -- 超预期程度 = 实际-预期
    surprise_direction TEXT,               -- 'positive'/'negative'/'neutral'

    created_at TEXT DEFAULT (datetime('now', '+8 hours')),
    UNIQUE(indicator_date, indicator_name)
);

-- ============================================================
-- 5. derivatives_data - 衍生品数据（日频）
-- ============================================================
CREATE TABLE IF NOT EXISTS derivatives_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trade_date TEXT NOT NULL,
    available_at TEXT NOT NULL,

    -- 期权PCR
    hs300_pcr_volume REAL,                -- 沪深300成交量PCR
    hs300_pcr_position REAL,              -- 沪深300持仓量PCR
    zz1000_pcr_position REAL,             -- 中证1000持仓量PCR

    -- 隐含波动率
    hs300_iv_near REAL,                   -- 沪深300近月IV
    hs300_iv_far REAL,                    -- 沪深300远月IV
    hs300_iv_change REAL,                 -- IV日变化
    hs300_iv_term_spread REAL,            -- IV期限结构(近-远)
    zz1000_iv_near REAL,                  -- 中证1000近月IV

    -- Skew
    hs300_skew_25d REAL,                  -- 25Delta Skew
    zz1000_skew_25d REAL,                 -- 中证1000 25Delta Skew

    -- 股指期货基差
    basis_if REAL,                        -- IF基差(%)
    basis_ic REAL,                        -- IC基差(%)
    basis_im REAL,                        -- IM基差(%)
    basis_ih REAL,                        -- IH基差(%)
    basis_divergence REAL,                -- IF-IC基差分化

    -- 期权持仓异动
    top5_strike_position TEXT,            -- Top5行权价持仓JSON
    position_anomaly_flag INTEGER,       -- 持仓异动标记(0/1)

    -- 到期日效应
    days_to_expiry INTEGER,               -- 距到期日天数
    expiry_week_flag INTEGER,             -- 是否到期周(0/1)
    max_position_strike REAL,             -- 最大持仓行权价

    created_at TEXT DEFAULT (datetime('now', '+8 hours')),
    UNIQUE(trade_date)
);

-- ============================================================
-- 6. signal_log - 信号日志（追踪准确率和衰减）
-- ============================================================
CREATE TABLE IF NOT EXISTS signal_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trade_date TEXT NOT NULL,
    signal_layer TEXT NOT NULL,           -- 'L0'/'L1'/'L2'/'L3'/'L4'/'L5'
    signal_name TEXT NOT NULL,            -- 信号名称
    signal_value REAL,                    -- 信号值
    signal_direction TEXT,               -- 'bullish'/'bearish'/'neutral'
    signal_strength REAL,                 -- 信号强度(0-1)
    signal_confidence REAL,              -- 置信度

    -- 预测记录
    predicted_direction TEXT,             -- 预测方向
    predicted_horizon TEXT,               -- '1d'/'3d'/'5d'/'20d'

    -- 实际结果（事后回填）
    actual_return_1d REAL,               -- T+1实际收益
    actual_return_3d REAL,               -- T+3实际收益
    actual_return_5d REAL,               -- T+5实际收益
    correct_flag INTEGER,                -- 方向是否正确(0/1)

    -- 衰减追踪
    ic_value REAL,                        -- 信息系数
    ic_decay_3d REAL,                    -- 3天后IC衰减
    ic_decay_5d REAL,                    -- 5天后IC衰减

    created_at TEXT DEFAULT (datetime('now', '+8 hours'))
);

-- ============================================================
-- 7. circuit_breaker_log - 熔断日志
-- ============================================================
CREATE TABLE IF NOT EXISTS circuit_breaker_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trigger_date TEXT NOT NULL,
    level INTEGER NOT NULL,               -- 1=降权, 2=暂停, 3=冻结
    reason TEXT NOT NULL,                 -- 触发原因
    consecutive_misses INTEGER,           -- 连续误判次数
    daily_loss_pct REAL,                  -- 当日亏损幅度
    systemic_risk_flag INTEGER,           -- 系统性风险标记
    action_taken TEXT,                    -- 执行动作
    recovery_date TEXT,                   -- 恢复日期
    duration_days INTEGER,                -- 持续天数

    created_at TEXT DEFAULT (datetime('now', '+8 hours'))
);

-- ============================================================
-- 8. data_source_log - 数据源状态日志（熔断降级）
-- ============================================================
CREATE TABLE IF NOT EXISTS data_source_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trade_date TEXT NOT NULL,
    source_name TEXT NOT NULL,            -- 'hithink'/'eastmoney'/'wind'/'csmar'
    layer TEXT NOT NULL,                  -- 对应信号层
    status TEXT NOT NULL,                 -- 'ok'/'delayed'/'failed'/'degraded'
    latency_ms INTEGER,                   -- 延迟毫秒
    error_message TEXT,                   -- 错误信息
    fallback_used TEXT,                   -- 使用的降级方案

    created_at TEXT DEFAULT (datetime('now', '+8 hours'))
);

-- ============================================================
-- 索引
-- ============================================================
CREATE INDEX IF NOT EXISTS idx_snapshot_date ON market_snapshot(trade_date);
CREATE INDEX IF NOT EXISTS idx_capital_date ON capital_flow(trade_date);
CREATE INDEX IF NOT EXISTS idx_limitup_date ON limit_up_pool(trade_date);
CREATE INDEX IF NOT EXISTS idx_macro_date ON macro_indicators(indicator_date);
CREATE INDEX IF NOT EXISTS idx_macro_name ON macro_indicators(indicator_name);
CREATE INDEX IF NOT EXISTS idx_deriv_date ON derivatives_data(trade_date);
CREATE INDEX IF NOT EXISTS idx_signal_date ON signal_log(trade_date);
CREATE INDEX IF NOT EXISTS idx_signal_layer ON signal_log(signal_layer);
CREATE INDEX IF NOT EXISTS idx_cb_date ON circuit_breaker_log(trigger_date);
CREATE INDEX IF NOT EXISTS idx_source_date ON data_source_log(trade_date);

-- ============================================================
-- 视图：最新市场快照
-- ============================================================
CREATE VIEW IF NOT EXISTS v_latest_snapshot AS
SELECT * FROM market_snapshot
ORDER BY trade_date DESC
LIMIT 1;

-- 视图：信号准确率统计
CREATE VIEW IF NOT EXISTS v_signal_accuracy AS
SELECT
    signal_layer,
    signal_name,
    COUNT(*) as total_signals,
    SUM(CASE WHEN correct_flag = 1 THEN 1 ELSE 0 END) as correct_count,
    ROUND(AVG(CASE WHEN correct_flag IS NOT NULL THEN correct_flag ELSE NULL END) * 100, 2) as accuracy_pct,
    AVG(ic_value) as avg_ic,
    AVG(ic_decay_3d) as avg_ic_decay_3d,
    AVG(ic_decay_5d) as avg_ic_decay_5d
FROM signal_log
WHERE correct_flag IS NOT NULL
GROUP BY signal_layer, signal_name;
