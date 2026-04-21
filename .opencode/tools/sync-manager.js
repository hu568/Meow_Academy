const MeowAcademyDB = require('./database');

class SyncManager {
    constructor(dbPath = '喵学堂.db') {
        this.db = new MeowAcademyDB(dbPath);
    }

    /**
     * 同步策略说明：
     * 1. SQLite 是数据源（Source of Truth）
     * 2. Markdown 是只读视图（Read-only View）
     * 3. 所有写操作都通过 SQLite 进行
     * 4. Markdown 通过 exportToMarkdown() 自动生成
     * 
     * 使用方式：
     * - AI/程序操作：直接读写 SQLite
     * - 人类阅读：查看 Markdown 文件
     * - 需要修改时：修改 SQLite，然后重新生成 Markdown
     */

    // 添加新学科
    async addSubject(id, name, description = '') {
        const now = new Date().toISOString();
        await this.db.run(
            `INSERT INTO subjects (id, name, description, created_at, updated_at) VALUES (?, ?, ?, ?, ?)`,
            [id, name, description, now, now]
        );
        console.log(`✅ 学科已添加：${name}`);
        await this.syncMarkdown();
    }

    // 添加新资料
    async addMaterial(id, subjectId, name, sourceType, chapter, knowledgePointsCount = 0, termsCount = 0) {
        const now = new Date().toISOString();
        await this.db.run(
            `INSERT INTO materials (id, subject_id, name, source_type, chapter, knowledge_points_count, terms_count, status, created_at, updated_at) 
             VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
            [id, subjectId, name, sourceType, chapter, knowledgePointsCount, termsCount, '待归档', now, now]
        );
        console.log(`✅ 资料已添加：${name}`);
        await this.syncMarkdown();
    }

    // 添加知识点卡片
    async addKnowledgeCard(id, materialId, name, difficulty, prerequisites = []) {
        const now = new Date().toISOString();
        await this.db.run(
            `INSERT INTO knowledge_cards (id, material_id, name, difficulty, prerequisites, created_at, updated_at) 
             VALUES (?, ?, ?, ?, ?, ?, ?)`,
            [id, materialId, name, difficulty, JSON.stringify(prerequisites), now, now]
        );
        console.log(`✅ 知识点卡片已添加：${name}`);
        await this.syncMarkdown();
    }

    // 添加专业词条
    async addTerm(id, term, category, relatedTerms = []) {
        const now = new Date().toISOString();
        await this.db.run(
            `INSERT INTO terms (id, term, category, related_terms, created_at, updated_at) 
             VALUES (?, ?, ?, ?, ?, ?)`,
            [id, term, category, JSON.stringify(relatedTerms), now, now]
        );
        console.log(`✅ 专业词条已添加：${term}`);
        await this.syncMarkdown();
    }

    // 归档资料
    async archiveMaterial(materialId) {
        const now = new Date().toISOString();
        await this.db.run(
            `UPDATE materials SET status = '已归档', archived_at = ? WHERE id = ?`,
            [now, materialId]
        );
        console.log(`✅ 资料已归档：${materialId}`);
        await this.syncMarkdown();
    }

    // 添加归档记录
    async addArchiveLog(operation, details, operator) {
        const now = new Date().toISOString();
        await this.db.run(
            `INSERT INTO archive_logs (operation, details, operator, created_at) VALUES (?, ?, ?, ?)`,
            [operation, details, operator, now]
        );
        console.log(`✅ 归档记录已添加`);
        await this.syncMarkdown();
    }

    // 同步 Markdown（重新生成）
    async syncMarkdown() {
        await this.db.exportToMarkdown('索引/图书总录.md');
        console.log('🔄 Markdown 已同步');
    }

    // 查询接口
    async query(sql, params = []) {
        return await this.db.query(sql, params);
    }

    // 获取统计信息
    async getStats() {
        return await this.db.query(`
            SELECT 
                (SELECT COUNT(*) FROM subjects) as 学科数,
                (SELECT COUNT(*) FROM materials) as 资料总数,
                (SELECT COUNT(*) FROM materials WHERE status = '已归档') as 已归档资料数,
                (SELECT COUNT(*) FROM knowledge_cards) as 知识点卡片总数,
                (SELECT COUNT(*) FROM terms) as 专业词条总数
        `);
    }

    // 获取完整学科信息
    async getSubjectDetail(subjectId) {
        const subject = await this.db.query('SELECT * FROM subjects WHERE id = ?', [subjectId]);
        const materials = await this.db.query('SELECT * FROM materials WHERE subject_id = ?', [subjectId]);
        const cards = await this.db.query(
            `SELECT k.* FROM knowledge_cards k 
             JOIN materials m ON k.material_id = m.id 
             WHERE m.subject_id = ?`, 
            [subjectId]
        );
        const terms = await this.db.query('SELECT * FROM terms');
        
        return {
            subject: subject[0],
            materials,
            knowledgeCards: cards,
            terms
        };
    }

    // 关闭连接
    async close() {
        await this.db.close();
    }
}

module.exports = SyncManager;
