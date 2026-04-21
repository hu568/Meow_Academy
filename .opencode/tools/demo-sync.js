const SyncManager = require('./sync-manager');

// 演示同步管理器的使用
const demo = async () => {
    const sync = new SyncManager('喵学堂.db');

    console.log('🚀 演示：喵学堂数据库同步管理器\n');

    // 1. 查看当前统计
    console.log('📊 当前统计：');
    const stats = await sync.getStats();
    console.table(stats);

    // 2. 添加新学科
    console.log('\n📚 添加新学科：数字电路');
    await sync.addSubject('digital-circuit', '数字电路', '数字电子技术基础');

    // 3. 添加新资料
    console.log('\n📖 添加新资料：');
    await sync.addMaterial(
        'digital-circuit-001',
        'digital-circuit',
        '逻辑门电路基础',
        '教材',
        '1.1',
        3,
        5
    );

    // 4. 添加知识点卡片
    console.log('\n🧩 添加知识点卡片：');
    await sync.addKnowledgeCard(
        'digital-circuit-001-001',
        'digital-circuit-001',
        '基本逻辑门',
        'easy',
        ['布尔代数']
    );
    await sync.addKnowledgeCard(
        'digital-circuit-001-002',
        'digital-circuit-001',
        'TTL逻辑门',
        'medium',
        ['基本逻辑门', '晶体管']
    );
    await sync.addKnowledgeCard(
        'digital-circuit-001-003',
        'digital-circuit-001',
        'CMOS逻辑门',
        'medium',
        ['基本逻辑门', 'MOS管']
    );

    // 5. 添加专业词条
    console.log('\n📖 添加专业词条：');
    await sync.addTerm('term-digital-001', '逻辑门', '数字电路基础', ['与门', '或门', '非门']);
    await sync.addTerm('term-digital-002', 'TTL', '数字电路技术', ['晶体管', '逻辑电平']);
    await sync.addTerm('term-digital-003', 'CMOS', '数字电路技术', ['MOS管', '低功耗']);

    // 6. 归档资料
    console.log('\n📦 归档资料：');
    await sync.archiveMaterial('digital-circuit-001');

    // 7. 添加归档记录
    console.log('\n📝 添加归档记录：');
    await sync.addArchiveLog(
        '新建数字电路学科，归档"1.1 逻辑门电路基础"',
        '内容：基本逻辑门、TTL逻辑门、CMOS逻辑门；产出：3张知识点卡片 + 3个专业词条',
        '西西喵斯'
    );

    // 8. 查看更新后的统计
    console.log('\n📊 更新后的统计：');
    const newStats = await sync.getStats();
    console.table(newStats);

    // 9. 查询数字电路学科详情
    console.log('\n🔍 数字电路学科详情：');
    const detail = await sync.getSubjectDetail('digital-circuit');
    console.log(`学科：${detail.subject.name}`);
    console.log(`资料数：${detail.materials.length}`);
    console.log(`知识点卡片数：${detail.knowledgeCards.length}`);
    console.log(`专业词条数：${detail.terms.length}`);

    await sync.close();
    console.log('\n✨ 演示完成！');
};

demo().catch(console.error);
