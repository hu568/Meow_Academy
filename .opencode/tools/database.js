const { createClient } = require('@libsql/client');
const fs = require('fs');
const path = require('path');

class MeowAcademyDB {
    constructor(dbPath = '喵学堂.db') {
        this.dbPath = dbPath;
        this.client = createClient({
            url: `file:${dbPath}`
        });
        this.initSchema();
    }

    async initSchema() {
        // 学科表
        await this.client.execute(`
            CREATE TABLE IF NOT EXISTS subjects (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        `);

        // 资料/书籍表
        await this.client.execute(`
            CREATE TABLE IF NOT EXISTS materials (
                id TEXT PRIMARY KEY,
                subject_id TEXT REFERENCES subjects(id),
                name TEXT NOT NULL,
                source_type TEXT,
                chapter TEXT,
                knowledge_points_count INTEGER DEFAULT 0,
                terms_count INTEGER DEFAULT 0,
                status TEXT DEFAULT '待归档',
                archived_at TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        `);

        // 知识点卡片表
        await this.client.execute(`
            CREATE TABLE IF NOT EXISTS knowledge_cards (
                id TEXT PRIMARY KEY,
                material_id TEXT REFERENCES materials(id),
                name TEXT NOT NULL,
                difficulty TEXT CHECK(difficulty IN ('easy', 'medium', 'hard')),
                prerequisites TEXT,
                content_summary TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        `);

        // 专业词典表
        await this.client.execute(`
            CREATE TABLE IF NOT EXISTS terms (
                id TEXT PRIMARY KEY,
                term TEXT NOT NULL,
                category TEXT,
                definition TEXT,
                related_terms TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        `);

        // 归档记录表
        await this.client.execute(`
            CREATE TABLE IF NOT EXISTS archive_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                operation TEXT NOT NULL,
                details TEXT,
                operator TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        `);

        // 创建索引
        await this.client.execute(`
            CREATE INDEX IF NOT EXISTS idx_materials_subject ON materials(subject_id)
        `);
        await this.client.execute(`
            CREATE INDEX IF NOT EXISTS idx_knowledge_cards_material ON knowledge_cards(material_id)
        `);
        await this.client.execute(`
            CREATE INDEX IF NOT EXISTS idx_terms_category ON terms(category)
        `);

        console.log('✅ 数据库表结构初始化完成');
    }

    // 导入现有数据
    async importFromMarkdown(data) {
        // 插入学科
        if (data.subject) {
            await this.client.execute({
                sql: `INSERT OR REPLACE INTO subjects (id, name, description, created_at, updated_at) VALUES (?, ?, ?, ?, ?)`,
                args: [
                    data.subject.id,
                    data.subject.name,
                    data.subject.description,
                    data.subject.created_at,
                    data.subject.updated_at
                ]
            });
        }

        // 插入资料
        if (data.materials) {
            for (const material of data.materials) {
                await this.client.execute({
                    sql: `INSERT OR REPLACE INTO materials 
                        (id, subject_id, name, source_type, chapter, knowledge_points_count, terms_count, status, archived_at, created_at, updated_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
                    args: [
                        material.id,
                        material.subject_id,
                        material.name,
                        material.source_type,
                        material.chapter,
                        material.knowledge_points_count,
                        material.terms_count,
                        material.status,
                        material.archived_at,
                        material.created_at,
                        material.updated_at
                    ]
                });
            }
        }

        // 插入知识点卡片
        if (data.knowledgeCards) {
            for (const card of data.knowledgeCards) {
                await this.client.execute({
                    sql: `INSERT OR REPLACE INTO knowledge_cards 
                        (id, material_id, name, difficulty, prerequisites, created_at, updated_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?)`,
                    args: [
                        card.id,
                        card.material_id,
                        card.name,
                        card.difficulty,
                        JSON.stringify(card.prerequisites),
                        card.created_at,
                        card.updated_at
                    ]
                });
            }
        }

        // 插入专业词条
        if (data.terms) {
            for (const term of data.terms) {
                await this.client.execute({
                    sql: `INSERT OR REPLACE INTO terms 
                        (id, term, category, related_terms, created_at, updated_at)
                        VALUES (?, ?, ?, ?, ?, ?)`,
                    args: [
                        term.id,
                        term.term,
                        term.category,
                        JSON.stringify(term.related_terms),
                        term.created_at,
                        term.updated_at
                    ]
                });
            }
        }

        // 插入归档记录
        if (data.archiveLogs) {
            for (const log of data.archiveLogs) {
                await this.client.execute({
                    sql: `INSERT INTO archive_logs (operation, details, operator, created_at) VALUES (?, ?, ?, ?)`,
                    args: [
                        log.operation,
                        log.details,
                        log.operator,
                        log.created_at
                    ]
                });
            }
        }

        console.log('✅ 数据导入完成');
    }

    // 导出为Markdown
    async exportToMarkdown(outputPath = '索引/图书总录.md') {
        const subjects = await this.query('SELECT * FROM subjects ORDER BY created_at');
        const materials = await this.query('SELECT * FROM materials ORDER BY created_at');
        const knowledgeCards = await this.query('SELECT * FROM knowledge_cards ORDER BY id');
        const terms = await this.query('SELECT * FROM terms ORDER BY term');
        const archiveLogs = await this.query('SELECT * FROM archive_logs ORDER BY created_at DESC');

        // 计算统计信息
        const statsResult = await this.query(`
            SELECT 
                (SELECT COUNT(*) FROM subjects) as subject_count,
                (SELECT COUNT(*) FROM materials WHERE status = '已归档') as archived_count,
                (SELECT COUNT(*) FROM knowledge_cards) as card_count,
                (SELECT COUNT(*) FROM terms) as term_count
        `);
        const stats = statsResult[0];

        let markdown = `# 图书总录\n\n`;
        markdown += `> 喵学堂知识库书籍/资料索引总表\n`;
        markdown += `> 最后更新：${new Date().toISOString().split('T')[0]}\n\n`;
        markdown += `---\n\n`;

        // 按学科分组输出
        for (const subject of subjects) {
            markdown += `## 📚 ${subject.name}\n\n`;

            // 该学科的资料
            const subjectMaterials = materials.filter(m => m.subject_id === subject.id);
            
            if (subjectMaterials.length > 0) {
                markdown += `### 课程笔记\n\n`;
                markdown += `| ID | 名称 | 来源类型 | 章节 | 知识点数 | 词条数 | 状态 | 日期 |\n`;
                markdown += `|----|------|----------|------|----------|--------|------|------|\n`;
                
                for (const material of subjectMaterials) {
                    const date = material.archived_at ? material.archived_at.split('T')[0] : '';
                    const status = material.status === '已归档' ? '✅ 已归档' : material.status;
                    markdown += `| ${material.id} | ${material.name} | ${material.source_type} | ${material.chapter} | ${material.knowledge_points_count} | ${material.terms_count} | ${status} | ${date} |\n`;
                }
                markdown += `\n`;

                // 知识点卡片清单
                markdown += `### 知识点卡片清单\n\n`;
                for (const material of subjectMaterials) {
                    const materialCards = knowledgeCards.filter(k => k.material_id === material.id);
                    if (materialCards.length > 0) {
                        markdown += `#### ${material.chapter} ${material.name}\n\n`;
                        markdown += `| 卡片ID | 名称 | 难度 | 前置知识 |\n`;
                        markdown += `|--------|------|------|----------|\n`;
                        
                        for (const card of materialCards) {
                            const prerequisites = card.prerequisites ? JSON.parse(card.prerequisites).join('、') : '';
                            markdown += `| ${card.id} | ${card.name} | ${card.difficulty} | ${prerequisites} |\n`;
                        }
                        markdown += `\n`;
                    }
                }

                // 专业词典清单
                const subjectTerms = terms.filter(t => {
                    return t.category && t.category.includes(subject.name);
                });
                
                if (subjectTerms.length > 0) {
                    markdown += `### 专业词典清单\n\n`;
                    markdown += `| 词条 | 分类 | 相关词条 |\n`;
                    markdown += `|------|------|----------|\n`;
                    
                    for (const term of subjectTerms) {
                        const related = term.related_terms ? JSON.parse(term.related_terms).join('、') : '';
                        markdown += `| ${term.term} | ${term.category} | ${related} |\n`;
                    }
                    markdown += `\n`;
                }
            }
        }

        // 统计信息
        markdown += `---\n\n`;
        markdown += `## 📊 统计信息\n\n`;
        markdown += `| 指标 | 数量 |\n`;
        markdown += `|------|------|\n`;
        markdown += `| 学科数 | ${stats.subject_count} |\n`;
        markdown += `| 已归档资料数 | ${stats.archived_count} |\n`;
        markdown += `| 知识点卡片总数 | ${stats.card_count} |\n`;
        markdown += `| 专业词条总数 | ${stats.term_count} |\n`;
        markdown += `\n---\n\n`;

        // 归档记录
        markdown += `## 📝 归档记录\n\n`;
        for (const log of archiveLogs) {
            const date = log.created_at.split('T')[0];
            markdown += `### ${date}\n`;
            markdown += `- **操作**：${log.operation}\n`;
            markdown += `- **详情**：${log.details}\n`;
            markdown += `- **操作者**：${log.operator}\n\n`;
        }

        markdown += `---\n\n`;
        markdown += `> 💡 **提示**：新增资料后请及时更新此索引表\n`;
        markdown += `> 🗄️ **数据库**：此文件由 SQLite 数据库自动生成，请勿手动编辑\n`;

        // 确保目录存在
        const dir = path.dirname(outputPath);
        if (!fs.existsSync(dir)) {
            fs.mkdirSync(dir, { recursive: true });
        }

        fs.writeFileSync(outputPath, markdown, 'utf8');
        console.log(`✅ Markdown 文件已生成：${outputPath}`);
        
        return markdown;
    }

    // 查询接口
    async query(sql, params = []) {
        const result = await this.client.execute({ sql, args: params });
        return result.rows;
    }

    // 执行接口
    async run(sql, params = []) {
        return await this.client.execute({ sql, args: params });
    }

    // 关闭数据库
    async close() {
        await this.client.close();
    }
}

module.exports = MeowAcademyDB;
