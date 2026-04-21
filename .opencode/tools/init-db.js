const MeowAcademyDB = require('./database');

// 初始化数据库
const db = new MeowAcademyDB('喵学堂.db');

// 从现有 Markdown 解析数据并导入
const importExistingData = async () => {
    // 模拟电路学科
    const subjectData = {
        id: 'analog-circuit',
        name: '模拟电路',
        description: '模拟电子技术基础',
        created_at: '2026-04-21T00:00:00Z',
        updated_at: '2026-04-21T00:00:00Z'
    };

    // 资料数据
    const materialsData = [
        {
            id: 'analog-circuit-004',
            subject_id: 'analog-circuit',
            name: '二极管和整流电路',
            source_type: '手写笔记',
            chapter: '4.1',
            knowledge_points_count: 4,
            terms_count: 9,
            status: '已归档',
            archived_at: '2026-04-21T00:00:00Z',
            created_at: '2026-04-21T00:00:00Z',
            updated_at: '2026-04-21T00:00:00Z'
        }
    ];

    // 知识点卡片数据
    const knowledgeCardsData = [
        {
            id: 'analog-circuit-004-001',
            material_id: 'analog-circuit-004',
            name: '半导体二极管基础',
            difficulty: 'easy',
            prerequisites: ['半导体物理基础', 'PN结原理'],
            created_at: '2026-04-21T00:00:00Z',
            updated_at: '2026-04-21T00:00:00Z'
        },
        {
            id: 'analog-circuit-004-002',
            material_id: 'analog-circuit-004',
            name: '二极管的伏安特性',
            difficulty: 'easy',
            prerequisites: ['二极管基础', '欧姆定律'],
            created_at: '2026-04-21T00:00:00Z',
            updated_at: '2026-04-21T00:00:00Z'
        },
        {
            id: 'analog-circuit-004-003',
            material_id: 'analog-circuit-004',
            name: '二极管的主要参数',
            difficulty: 'medium',
            prerequisites: ['伏安特性', '功率计算'],
            created_at: '2026-04-21T00:00:00Z',
            updated_at: '2026-04-21T00:00:00Z'
        },
        {
            id: 'analog-circuit-004-004',
            material_id: 'analog-circuit-004',
            name: '稳压二极管',
            difficulty: 'medium',
            prerequisites: ['伏安特性', '反向击穿', '欧姆定律'],
            created_at: '2026-04-21T00:00:00Z',
            updated_at: '2026-04-21T00:00:00Z'
        }
    ];

    // 专业词典数据
    const termsData = [
        {
            id: 'term-001',
            term: '本征半导体',
            category: '半导体物理',
            related_terms: ['掺杂半导体', '载流子', 'PN结'],
            created_at: '2026-04-21T00:00:00Z',
            updated_at: '2026-04-21T00:00:00Z'
        },
        {
            id: 'term-002',
            term: '掺杂半导体',
            category: '半导体物理',
            related_terms: ['本征半导体', 'N型/P型半导体'],
            created_at: '2026-04-21T00:00:00Z',
            updated_at: '2026-04-21T00:00:00Z'
        },
        {
            id: 'term-003',
            term: 'PN结',
            category: '半导体器件',
            related_terms: ['二极管', '空间电荷区', '单向导电性'],
            created_at: '2026-04-21T00:00:00Z',
            updated_at: '2026-04-21T00:00:00Z'
        },
        {
            id: 'term-004',
            term: '死区电压',
            category: '二极管特性',
            related_terms: ['导通电压', '伏安特性', '硅管/锗管'],
            created_at: '2026-04-21T00:00:00Z',
            updated_at: '2026-04-21T00:00:00Z'
        },
        {
            id: 'term-005',
            term: '整流电流',
            category: '二极管参数',
            related_terms: ['最大整流电流', '正向电流'],
            created_at: '2026-04-21T00:00:00Z',
            updated_at: '2026-04-21T00:00:00Z'
        },
        {
            id: 'term-006',
            term: '反向工作电压',
            category: '二极管参数',
            related_terms: ['最高反向工作电压', '反向击穿'],
            created_at: '2026-04-21T00:00:00Z',
            updated_at: '2026-04-21T00:00:00Z'
        },
        {
            id: 'term-007',
            term: '反向电流',
            category: '二极管参数',
            related_terms: ['漏电流', '最大反向电流'],
            created_at: '2026-04-21T00:00:00Z',
            updated_at: '2026-04-21T00:00:00Z'
        },
        {
            id: 'term-008',
            term: '稳压二极管',
            category: '半导体器件',
            related_terms: ['齐纳二极管', '稳压电路', '动态电阻'],
            created_at: '2026-04-21T00:00:00Z',
            updated_at: '2026-04-21T00:00:00Z'
        },
        {
            id: 'term-009',
            term: '动态电阻',
            category: '器件参数',
            related_terms: ['稳压二极管', '交流电阻', '小信号模型'],
            created_at: '2026-04-21T00:00:00Z',
            updated_at: '2026-04-21T00:00:00Z'
        }
    ];

    // 归档记录数据
    const archiveLogsData = [
        {
            operation: '新建模拟电路学科，归档"4.1 二极管和整流电路"手写笔记',
            details: '内容：半导体基础、二极管原理、伏安特性、主要参数、稳压二极管；产出：4张知识点卡片 + 9个专业词条',
            operator: '西西喵斯（帕秋莉代理）',
            created_at: '2026-04-21T00:00:00Z'
        }
    ];

    // 导入数据
    await db.importFromMarkdown({
        subject: subjectData,
        materials: materialsData,
        knowledgeCards: knowledgeCardsData,
        terms: termsData,
        archiveLogs: archiveLogsData
    });

    console.log('✅ 现有数据导入完成');
};

// 生成 Markdown 文件
const generateMarkdown = async () => {
    await db.exportToMarkdown('索引/图书总录.md');
};

// 主流程
const main = async () => {
    console.log('🚀 开始初始化喵学堂数据库...\n');

    await importExistingData();
    await generateMarkdown();

    console.log('\n✨ 初始化完成！');
    console.log('📁 数据库文件：喵学堂.db');
    console.log('📄 Markdown文件：索引/图书总录.md');

    // 演示查询
    console.log('\n🔍 演示查询 - 所有知识点卡片：');
    const cards = await db.query('SELECT id, name, difficulty FROM knowledge_cards');
    console.table(cards);

    console.log('\n🔍 演示查询 - 统计信息：');
    const stats = await db.query(`
        SELECT 
            (SELECT COUNT(*) FROM subjects) as 学科数,
            (SELECT COUNT(*) FROM materials WHERE status = '已归档') as 已归档资料数,
            (SELECT COUNT(*) FROM knowledge_cards) as 知识点卡片总数,
            (SELECT COUNT(*) FROM terms) as 专业词条总数
    `);
    console.table(stats);

    await db.close();
    console.log('\n👋 数据库连接已关闭');
};

main().catch(console.error);
