// 全局变量
const API_BASE_URL = 'http://localhost:8000/api/v1';
let currentModal = null;

// DOM 加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    checkSystemStatus();
});

// 初始化事件监听器
function initializeEventListeners() {
    // 功能卡片点击事件
    document.querySelectorAll('.feature-card').forEach(card => {
        card.addEventListener('click', function() {
            const cardType = this.dataset.type;
            openModal(cardType);
        });
    });

    // 主要操作按钮
    document.getElementById('analyzeBtn').addEventListener('click', () => openModal('analyze'));
    document.getElementById('generateBtn').addEventListener('click', () => openModal('generate'));
    document.getElementById('communityBtn').addEventListener('click', () => openModal('community'));
    
    // 新增市场调研按钮
    const researchBtn = document.getElementById('researchBtn');
    if (researchBtn) {
        researchBtn.addEventListener('click', () => openModal('research'));
    }

    // 模态框关闭事件
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('modal-overlay') || e.target.classList.contains('close-btn')) {
            closeModal();
        }
    });

    // ESC 键关闭模态框
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && currentModal) {
            closeModal();
        }
    });
}

// 检查系统状态
async function checkSystemStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/status`);
        const data = await response.json();
        
        if (data.status === 'operational' || data.status === 'healthy') {
            updateStatusBadges('运行中');
        } else {
            updateStatusBadges('离线');
        }
    } catch (error) {
        console.error('系统状态检查失败:', error);
        updateStatusBadges('离线');
    }
}

// 更新状态徽章
function updateStatusBadges(status) {
    document.querySelectorAll('.status-badge').forEach(badge => {
        badge.textContent = status;
        badge.className = status === '运行中' ? 'status-badge' : 'status-badge offline';
    });
}

// 打开模态框
function openModal(type) {
    const modalContent = getModalContent(type);
    
    const modalHTML = `
        <div class="modal-overlay">
            <div class="modal">
                <div class="modal-header">
                    <h3 class="modal-title">${modalContent.title}</h3>
                    <button class="close-btn">&times;</button>
                </div>
                <div class="modal-body">
                    ${modalContent.body}
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    currentModal = document.querySelector('.modal-overlay:last-child');
    
    // 显示模态框
    setTimeout(() => {
        currentModal.style.opacity = '1';
        currentModal.style.visibility = 'visible';
    }, 10);
    
    // 绑定表单提交事件
    const form = currentModal.querySelector('form');
    if (form) {
        form.addEventListener('submit', (e) => handleFormSubmit(e, type));
    }
}

// 关闭模态框
function closeModal() {
    if (currentModal) {
        currentModal.style.opacity = '0';
        currentModal.style.visibility = 'hidden';
        setTimeout(() => {
            currentModal.remove();
            currentModal = null;
        }, 300);
    }
}

// 获取模态框内容
function getModalContent(type) {
    const contents = {
        analyze: {
            title: '🔍 用户分析',
            body: `
                <form id="analyzeForm">
                    <div class="form-group">
                        <label class="form-label">GitHub 用户名</label>
                        <input type="text" class="form-input" name="username" placeholder="例如: octocat" required>
                        <div class="form-help">输入要分析的 GitHub 用户名</div>
                    </div>
                    <div class="form-group">
                        <label class="form-label">分析深度</label>
                        <select class="form-select" name="depth">
                            <option value="basic">基础分析</option>
                            <option value="deep">深度分析</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">报告语言</label>
                        <select class="form-select" name="language">
                            <option value="zh">中文</option>
                            <option value="en">English</option>
                        </select>
                    </div>
                    <button type="submit" class="btn btn-primary">
                        <span class="btn-icon">🚀</span>
                        开始分析
                    </button>
                </form>
            `
        },
        generate: {
            title: '✨ AI 内容生成',
            body: `
                <form id="generateForm">
                    <div class="form-group">
                        <label class="form-label">内容类型</label>
                        <select class="form-select" name="content_type" required>
                            <option value="">选择内容类型</option>
                            <option value="blog_post">博客文章</option>
                            <option value="social_media">社交媒体</option>
                            <option value="email">邮件营销</option>
                            <option value="documentation">技术文档</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">主题</label>
                        <input type="text" class="form-input" name="topic" placeholder="例如: React 最佳实践" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label">目标受众</label>
                        <input type="text" class="form-input" name="target_audience" placeholder="例如: 前端开发者">
                    </div>
                    <div class="form-group">
                        <label class="form-label">关键词</label>
                        <input type="text" class="form-input" name="keywords" placeholder="用逗号分隔，例如: React, 性能优化, 最佳实践">
                    </div>
                    <div class="form-group">
                        <label class="form-label">语言</label>
                        <select class="form-select" name="language">
                            <option value="zh">中文</option>
                            <option value="en">English</option>
                        </select>
                    </div>
                    <button type="submit" class="btn btn-primary">
                        <span class="btn-icon">✨</span>
                        生成内容
                    </button>
                </form>
            `
        },
        community: {
            title: '🤝 社区互动',
            body: `
                <form id="communityForm">
                    <div class="form-group">
                        <label class="form-label">目标仓库</label>
                        <input type="text" class="form-input" name="repository" placeholder="例如: facebook/react" required>
                        <div class="form-help">格式: owner/repo</div>
                    </div>
                    <div class="form-group">
                        <label class="form-label">互动类型</label>
                        <select class="form-select" name="interaction_types" multiple>
                            <option value="star">Star 项目</option>
                            <option value="follow">关注用户</option>
                            <option value="comment">评论互动</option>
                            <option value="issue">创建 Issue</option>
                        </select>
                        <div class="form-help">按住 Ctrl/Cmd 可多选</div>
                    </div>
                    <div class="form-group">
                        <label class="form-label">回溯天数</label>
                        <input type="number" class="form-input" name="lookback_days" value="30" min="1" max="365">
                    </div>
                    <div class="form-group">
                        <label class="form-label">语言</label>
                        <select class="form-select" name="language">
                            <option value="zh">中文</option>
                            <option value="en">English</option>
                        </select>
                    </div>
                    <button type="submit" class="btn btn-primary">
                        <span class="btn-icon">🤝</span>
                        开始互动
                    </button>
                </form>
            `
        },
        campaign: {
            title: '📈 营销活动',
            body: `
                <form id="campaignForm">
                    <div class="form-group">
                        <label class="form-label">活动名称</label>
                        <input type="text" class="form-input" name="campaign_name" placeholder="例如: React 开发者推广活动" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label">目标受众</label>
                        <textarea class="form-textarea" name="target_audience" placeholder="描述您的目标受众..."></textarea>
                    </div>
                    <div class="form-group">
                        <label class="form-label">营销目标</label>
                        <select class="form-select" name="goals" multiple>
                            <option value="brand_awareness">品牌知名度</option>
                            <option value="user_acquisition">用户获取</option>
                            <option value="community_growth">社区增长</option>
                            <option value="engagement">用户参与</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">预算范围</label>
                        <select class="form-select" name="budget">
                            <option value="low">低预算 (< $1000)</option>
                            <option value="medium">中等预算 ($1000-$5000)</option>
                            <option value="high">高预算 (> $5000)</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">语言</label>
                        <select class="form-select" name="language">
                            <option value="zh">中文</option>
                            <option value="en">English</option>
                        </select>
                    </div>
                    <button type="submit" class="btn btn-primary">
                        <span class="btn-icon">📈</span>
                        创建活动
                    </button>
                </form>
            `
        },
        research: {
            title: '📊 市场调研',
            body: `
                <form id="researchForm">
                    <div class="form-group">
                        <label class="form-label">调研类型</label>
                        <select class="form-select" name="research_type" required>
                            <option value="">选择调研类型</option>
                            <option value="competitor">竞争对手分析</option>
                            <option value="technology">技术趋势研究</option>
                            <option value="market">市场趋势分析</option>
                            <option value="user_feedback">用户反馈分析</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">调研目标</label>
                        <input type="text" class="form-input" name="target" placeholder="例如: Great Expectations, 数据质量评估" required>
                        <div class="form-help">输入要调研的具体目标或关键词</div>
                    </div>
                    <div class="form-group">
                        <label class="form-label">调研深度</label>
                        <select class="form-select" name="depth">
                            <option value="shallow">浅层调研 (快速)</option>
                            <option value="medium">中等深度</option>
                            <option value="deep">深度调研 (详细)</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">报告语言</label>
                        <select class="form-select" name="language">
                            <option value="zh">中文</option>
                            <option value="en">English</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">附加要求 (可选)</label>
                        <textarea class="form-textarea" name="requirements" placeholder="例如: 重点关注开源项目，包含价格对比等"></textarea>
                    </div>
                    <button type="submit" class="btn btn-primary">
                        <span class="btn-icon">🔍</span>
                        开始调研
                    </button>
                </form>
            `
        }
    };
    
    return contents[type] || { title: '功能', body: '<p>功能开发中...</p>' };
}

// 处理表单提交
async function handleFormSubmit(e, type) {
    e.preventDefault();
    
    const form = e.target;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    
    // 处理用户分析特殊字段映射
    if (type === 'analyze') {
        // 将username转换为user_list数组
        if (data.username) {
            data.user_list = [data.username.trim()];
            delete data.username;
        }
        // 将depth映射为analysis_depth
        if (data.depth) {
            data.analysis_depth = data.depth;
            delete data.depth;
        }
    }
    
    // 处理多选字段
    if (data.interaction_types) {
        data.interaction_types = formData.getAll('interaction_types');
    }
    if (data.goals) {
        data.goals = formData.getAll('goals');
    }
    
    // 处理关键词字段（转换为数组）
    if (data.keywords && typeof data.keywords === 'string') {
        data.keywords = data.keywords.split(',').map(k => k.trim()).filter(k => k);
    }
    
    // 显示加载状态
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<span class="loading"><span class="spinner"></span>处理中...</span>';
    submitBtn.disabled = true;
    
    try {
        const result = await callAPI(type, data);
        // 先关闭当前的表单模态框
        closeModal();
        // 然后显示结果模态框
        showResult(result, type);
    } catch (error) {
        // 改进错误处理，确保显示正确的错误消息
        let errorMessage = '操作失败';
        if (typeof error === 'string') {
            errorMessage = error;
        } else if (error && error.message) {
            errorMessage = error.message;
        } else if (error && typeof error === 'object') {
            errorMessage = JSON.stringify(error);
        }
        showError(errorMessage);
    } finally {
        // 恢复按钮状态
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }
}

// API 调用
async function callAPI(type, data) {
    const endpoints = {
        analyze: '/github/analyze',
        generate: '/content/generate',
        community: '/community/engage',
        campaign: '/marketing/comprehensive',
        research: '/research/enhanced'
    };
    
    const endpoint = endpoints[type];
    if (!endpoint) {
        throw new Error('未知的操作类型');
    }
    
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    });
    
    if (!response.ok) {
        let errorMessage = `请求失败: ${response.status}`;
        try {
            const errorData = await response.json();
            if (errorData.detail) {
                errorMessage = errorData.detail;
            } else if (errorData.message) {
                errorMessage = errorData.message;
            } else if (typeof errorData === 'string') {
                errorMessage = errorData;
            }
        } catch (parseError) {
            // JSON 解析失败，使用默认错误消息
            console.error('Error parsing response:', parseError);
        }
        throw new Error(errorMessage);
    }
    
    return await response.json();
}

// 显示结果
function showResult(result, type) {
    // 格式化结果内容
    let resultContent = '';
    
    if (type === 'research' && result.result) {
        // 市场调研结果
        resultContent = `
            <div class="result-summary">
                <h4>📊 调研摘要</h4>
                <div class="summary-grid">
                    <div class="summary-item">
                        <span class="label">调研ID:</span>
                        <span class="value">${result.research_id || '未知'}</span>
                    </div>
                    <div class="summary-item">
                        <span class="label">状态:</span>
                        <span class="value status-${result.status}">${result.status === 'completed' ? '已完成' : result.status}</span>
                    </div>
                    <div class="summary-item">
                        <span class="label">调研类型:</span>
                        <span class="value">${result.research_type || '未知'}</span>
                    </div>
                    <div class="summary-item">
                        <span class="label">目标:</span>
                        <span class="value">${result.target || '未知'}</span>
                    </div>
                </div>
            </div>
            <div class="result-details">
                <h4>📋 调研报告</h4>
                <div class="research-content">
                    <pre>${result.result}</pre>
                </div>
            </div>
            ${result.metadata ? `
                <div class="result-details">
                    <h4>📊 调研元数据</h4>
                    <div class="metadata-content">
                        <pre>${JSON.stringify(result.metadata, null, 2)}</pre>
                    </div>
                </div>
            ` : ''}
        `;
    } else if (result.engagement_result) {
        // 社区互动结果 - 优先检查，因为可能同时包含insights字段
        const engagement = result.engagement_result;
        const config = engagement.config || {};
        // 处理嵌套的 engagement_result 结构
        const engagementData = engagement.engagement_result || engagement;
        
        resultContent = `
            <div class="result-summary">
                <h4>🤝 互动摘要</h4>
                <div class="summary-grid">
                    <div class="summary-item">
                        <span class="label">目标仓库:</span>
                        <span class="value">${config.repository || '未知'}</span>
                    </div>
                    <div class="summary-item">
                        <span class="label">互动类型:</span>
                        <span class="value">${config.interaction_types?.join(', ') || '未知'}</span>
                    </div>
                    <div class="summary-item">
                        <span class="label">分析时间范围:</span>
                        <span class="value">${config.lookback_days || 30} 天</span>
                    </div>
                    <div class="summary-item">
                        <span class="label">目标用户数:</span>
                        <span class="value">${config.target_count || 10}</span>
                    </div>
                </div>
            </div>
            ${result.insights ? `
                <div class="result-details">
                    <h4>💡 执行洞察</h4>
                    <div class="insights-content">
                        <p>${result.insights}</p>
                    </div>
                </div>
            ` : ''}
            ${result.recommendations ? `
                <div class="result-details">
                    <h4>📋 建议事项</h4>
                    <div class="recommendations-content">
                        <ul>
                            ${result.recommendations.map(rec => `<li>${rec}</li>`).join('')}
                        </ul>
                    </div>
                </div>
            ` : ''}
            ${engagementData.raw ? `
                <div class="result-details">
                    <h4>📋 详细互动报告</h4>
                    <div class="activity-content">
                        <pre>${engagementData.raw}</pre>
                    </div>
                </div>
            ` : ''}
            ${engagementData.tasks_output && engagementData.tasks_output.length > 0 ? `
                <div class="result-details">
                    <h4>📊 任务执行详情</h4>
                    <div class="tasks-content">
                        ${engagementData.tasks_output.map((task, index) => `
                            <div class="task-item">
                                <h5>任务 ${index + 1}: ${task.agent || '未知代理'}</h5>
                                <div class="task-description">
                                    <strong>预期输出:</strong> ${task.expected_output || '未知'}
                                </div>
                                ${task.raw ? `
                                    <div class="task-output">
                                        <strong>执行结果:</strong>
                                        <pre>${task.raw}</pre>
                                    </div>
                                ` : ''}
                            </div>
                        `).join('')}
                    </div>
                </div>
            ` : ''}
            ${engagementData.token_usage ? `
                <div class="result-details">
                    <h4>📊 资源使用情况</h4>
                    <div class="token-usage">
                        <div class="usage-grid">
                            <div class="usage-item">
                                <span class="label">总Token数:</span>
                                <span class="value">${engagementData.token_usage.total_tokens?.toLocaleString() || 0}</span>
                            </div>
                            <div class="usage-item">
                                <span class="label">成功请求:</span>
                                <span class="value">${engagementData.token_usage.successful_requests || 0}</span>
                            </div>
                            <div class="usage-item">
                                <span class="label">提示Token:</span>
                                <span class="value">${engagementData.token_usage.prompt_tokens?.toLocaleString() || 0}</span>
                            </div>
                            <div class="usage-item">
                                <span class="label">完成Token:</span>
                                <span class="value">${engagementData.token_usage.completion_tokens?.toLocaleString() || 0}</span>
                            </div>
                        </div>
                    </div>
                </div>
            ` : ''}
        `;
    } else if (result.insights) {
        // 用户分析结果
        const insights = result.insights;
        resultContent = `
            <div class="result-summary">
                <h4>📊 分析摘要</h4>
                <div class="summary-grid">
                    <div class="summary-item">
                        <span class="label">分析用户数:</span>
                        <span class="value">${insights.total_users || 0}</span>
                    </div>
                    <div class="summary-item">
                        <span class="label">分析深度:</span>
                        <span class="value">${insights.analysis_depth || '基础'}</span>
                    </div>
                    <div class="summary-item">
                        <span class="label">报告语言:</span>
                        <span class="value">${insights.language === 'zh' ? '中文' : 'English'}</span>
                    </div>
                    <div class="summary-item">
                        <span class="label">完成时间:</span>
                        <span class="value">${insights.completion_time || '未知'}</span>
                    </div>
                </div>
            </div>
            ${insights.analysis_results ? `
                <div class="result-details">
                    <h4>📋 详细分析</h4>
                    <div class="analysis-content">
                        ${formatAnalysisResults(insights.analysis_results)}
                    </div>
                </div>
            ` : ''}
        `;
    } else if (result.content) {
        // 内容生成结果
        resultContent = `
            <div class="result-details">
                <h4>✨ 生成的内容</h4>
                <div class="generated-content">
                    <pre>${result.content}</pre>
                </div>
            </div>
        `;
    } else {
        // 通用结果显示
        resultContent = `
            <div class="result-details">
                <h4>📋 执行结果</h4>
                <pre>${JSON.stringify(result, null, 2)}</pre>
            </div>
        `;
    }

    const resultModal = `
        <div class="modal-overlay">
            <div class="modal result-modal">
                <div class="modal-header">
                    <h3 class="modal-title">✅ 操作成功</h3>
                    <button class="close-btn">&times;</button>
                </div>
                <div class="modal-body">
                    <div class="result-content">
                        <div class="basic-info">
                            <p><strong>任务ID:</strong> <code>${result.task_id || '未知'}</code></p>
                            <p><strong>状态:</strong> <span class="status-success">${result.status || '已提交'}</span></p>
                            ${result.message ? `<p><strong>消息:</strong> ${result.message}</p>` : ''}
                        </div>
                        ${resultContent}
                    </div>
                    <div class="modal-actions">
                        <button class="btn btn-secondary close-modal-btn">关闭</button>
                        <button class="btn btn-primary copy-result-btn">复制结果</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', resultModal);
    currentModal = document.querySelector('.modal-overlay:last-child');
    
    // 绑定所有关闭事件
    const closeBtn = currentModal.querySelector('.close-btn');
    const closeModalBtn = currentModal.querySelector('.close-modal-btn');
    const copyBtn = currentModal.querySelector('.copy-result-btn');
    const overlay = currentModal;
    
    // 关闭按钮事件
    if (closeBtn) {
        closeBtn.addEventListener('click', closeModal);
    }
    
    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', closeModal);
    }
    
    // 复制按钮事件
    if (copyBtn) {
        copyBtn.addEventListener('click', copyResultToClipboard);
    }
    
    // 点击遮罩层关闭
    overlay.addEventListener('click', function(e) {
        if (e.target === overlay) {
            closeModal();
        }
    });
}

// 格式化分析结果
function formatAnalysisResults(results) {
    if (typeof results === 'string') {
        return `<div class="analysis-text">${results}</div>`;
    } else if (Array.isArray(results)) {
        return results.map(item => `<div class="analysis-item">${JSON.stringify(item, null, 2)}</div>`).join('');
    } else {
        return `<pre>${JSON.stringify(results, null, 2)}</pre>`;
    }
}

// 复制结果到剪贴板
function copyResultToClipboard() {
    const resultContent = currentModal.querySelector('.result-content');
    if (resultContent) {
        const text = resultContent.innerText;
        copyToClipboard(text);
    }
}

// 显示错误
function showError(message) {
    const errorModal = `
        <div class="modal-overlay">
            <div class="modal">
                <div class="modal-header">
                    <h3 class="modal-title">❌ 操作失败</h3>
                    <button class="close-btn">&times;</button>
                </div>
                <div class="modal-body">
                    <div class="error-content">
                        <p style="color: #dc2626;">${message}</p>
                    </div>
                    <div style="margin-top: 1rem;">
                        <button class="btn btn-secondary close-modal-btn">关闭</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', errorModal);
    currentModal = document.querySelector('.modal-overlay:last-child');
    
    // 绑定关闭事件
    const closeBtn = currentModal.querySelector('.close-btn');
    const closeModalBtn = currentModal.querySelector('.close-modal-btn');
    const overlay = currentModal;
    
    if (closeBtn) {
        closeBtn.addEventListener('click', closeModal);
    }
    
    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', closeModal);
    }
    
    // 点击遮罩层关闭
    overlay.addEventListener('click', function(e) {
        if (e.target === overlay) {
            closeModal();
        }
    });
}

// 工具函数：格式化数字
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

// 工具函数：复制到剪贴板
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        showNotification('已复制到剪贴板');
    } catch (err) {
        console.error('复制失败:', err);
    }
}

// 显示通知
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#059669' : '#dc2626'};
        color: white;
        padding: 1rem;
        border-radius: 6px;
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// 添加 CSS 动画
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
    
    .result-details pre {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 6px;
        overflow-x: auto;
        font-size: 0.875rem;
        max-height: 300px;
        overflow-y: auto;
    }
    
    .status-badge.offline {
        background: #fee2e2;
        color: #dc2626;
    }
    
    /* 结果模态框样式 */
    .result-modal {
        max-width: 800px;
        max-height: 90vh;
        overflow-y: auto;
    }
    
    .basic-info {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 6px;
        margin-bottom: 1rem;
    }
    
    .basic-info code {
        background: #e5e7eb;
        padding: 2px 6px;
        border-radius: 3px;
        font-family: monospace;
        font-size: 0.875rem;
    }
    
    .status-success {
        color: #059669;
        font-weight: 600;
    }
    
    .result-summary {
        margin-bottom: 1.5rem;
    }
    
    .summary-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-top: 0.5rem;
    }
    
    .summary-item {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        padding: 0.75rem;
        border-radius: 6px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .summary-item .label {
        font-weight: 500;
        color: #6b7280;
    }
    
    .summary-item .value {
        font-weight: 600;
        color: #111827;
    }
    
    .result-details {
        margin-top: 1.5rem;
    }
    
    .result-details h4 {
        margin-bottom: 0.75rem;
        color: #374151;
        border-bottom: 2px solid #e5e7eb;
        padding-bottom: 0.5rem;
    }
    
    .analysis-content, .generated-content, .activity-content {
        background: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 6px;
        padding: 1rem;
        max-height: 400px;
        overflow-y: auto;
    }
    
    .analysis-text {
        line-height: 1.6;
        white-space: pre-wrap;
    }
    
    .analysis-item {
        margin-bottom: 1rem;
        padding: 0.75rem;
        background: #ffffff;
        border-radius: 4px;
        border-left: 3px solid #059669;
    }
    
    .modal-actions {
        margin-top: 1.5rem;
        display: flex;
        gap: 0.75rem;
        justify-content: flex-end;
        padding-top: 1rem;
        border-top: 1px solid #e5e7eb;
    }
    
    .modal-actions .btn {
        min-width: 100px;
    }
    
    /* 新增样式 */
    .insights-content {
        background: #f0f9ff;
        border: 1px solid #0ea5e9;
        border-radius: 6px;
        padding: 1rem;
        color: #0c4a6e;
        line-height: 1.6;
    }
    
    .recommendations-content {
        background: #f0fdf4;
        border: 1px solid #22c55e;
        border-radius: 6px;
        padding: 1rem;
    }
    
    .recommendations-content ul {
        margin: 0;
        padding-left: 1.5rem;
    }
    
    .recommendations-content li {
        margin-bottom: 0.5rem;
        color: #166534;
    }
    
    .token-usage {
        background: #fef3c7;
        border: 1px solid #f59e0b;
        border-radius: 6px;
        padding: 1rem;
    }
    
    .usage-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 0.75rem;
    }
    
    .usage-item {
        background: #ffffff;
        border: 1px solid #d97706;
        padding: 0.5rem;
        border-radius: 4px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .usage-item .label {
        font-weight: 500;
        color: #92400e;
        font-size: 0.875rem;
    }
    
    .usage-item .value {
        font-weight: 600;
        color: #451a03;
    }
    
    /* 新增任务详情样式 */
    .tasks-content {
        background: #f8fafc;
        border: 1px solid #cbd5e1;
        border-radius: 6px;
        padding: 1rem;
        max-height: 500px;
        overflow-y: auto;
    }
    
    .task-item {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 1rem;
        margin-bottom: 1rem;
        border-left: 4px solid #3b82f6;
    }
    
    .task-item:last-child {
        margin-bottom: 0;
    }
    
    .task-item h5 {
        margin: 0 0 0.75rem 0;
        color: #1e40af;
        font-size: 1rem;
        font-weight: 600;
    }
    
    .task-description {
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        border-radius: 4px;
        padding: 0.75rem;
        margin-bottom: 0.75rem;
        color: #1e40af;
        font-size: 0.875rem;
    }
    
    .task-output {
        background: #f1f5f9;
        border: 1px solid #cbd5e1;
        border-radius: 4px;
        padding: 0.75rem;
    }
    
    .task-output strong {
        color: #475569;
        font-size: 0.875rem;
        display: block;
        margin-bottom: 0.5rem;
    }
    
    .task-output pre {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 4px;
        padding: 0.75rem;
        margin: 0;
        font-size: 0.8rem;
        line-height: 1.4;
        max-height: 200px;
        overflow-y: auto;
        white-space: pre-wrap;
        word-wrap: break-word;
    }
`;
document.head.appendChild(style); 