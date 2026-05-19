import streamlit as st
import json
import os
import requests

st.set_page_config(
    page_title="校招岗位智能匹配系统",
    page_icon="💼",
    layout="wide"
)

# 后端 API 地址
API_URL = "http://127.0.0.1:5000/api"

DATA_FILE = "app_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return validate_data(data)
        except Exception as e:
            st.warning(f"数据加载失败，使用默认数据: {str(e)}")
            return get_default_data()
    return get_default_data()

def validate_data(data):
    required_keys = ["stats", "jobs", "resume_example", "optimizations"]
    for key in required_keys:
        if key not in data:
            st.warning(f"数据缺少 {key} 字段，使用默认值")
            return get_default_data()
    
    if not isinstance(data.get("jobs", []), list):
        data["jobs"] = get_default_data()["jobs"]
    
    if not isinstance(data.get("stats", {}), dict):
        data["stats"] = get_default_data()["stats"]
    
    for job in data.get("jobs", []):
        required_job_fields = ["id", "title", "company", "location", "salary", "industry", "matchScore"]
        for field in required_job_fields:
            if field not in job:
                job[field] = "未知" if field != "id" and field != "matchScore" else 0
    
    return data

def get_default_data():
    return {
        "stats": {
            "total_jobs": 12580,
            "total_students": 8900,
            "avg_match_rate": 87.3,
            "parse_time": "<5秒"
        },
        "jobs": [
            {"id": 1, "title": "前端开发工程师", "company": "字节跳动", "location": "北京", "salary": "15-25K", "industry": "互联网", "matchScore": 92, "skills": ["React", "TypeScript", "JavaScript", "CSS"], "experience": "应届", "degree": "本科"},
            {"id": 2, "title": "Java后端开发", "company": "阿里巴巴", "location": "杭州", "salary": "18-30K", "industry": "电商", "matchScore": 87, "skills": ["Java", "Spring Boot", "MySQL", "Redis"], "experience": "应届", "degree": "本科"},
            {"id": 3, "title": "产品经理", "company": "腾讯", "location": "深圳", "salary": "16-28K", "industry": "互联网", "matchScore": 85, "skills": ["需求分析", "产品设计", "原型设计", "数据分析"], "experience": "应届", "degree": "本科"},
            {"id": 4, "title": "算法工程师", "company": "百度", "location": "北京", "salary": "20-35K", "industry": "AI", "matchScore": 90, "skills": ["Python", "机器学习", "深度学习", "TensorFlow"], "experience": "应届", "degree": "硕士"},
            {"id": 5, "title": "数据分析师", "company": "美团", "location": "北京", "salary": "14-22K", "industry": "本地生活", "matchScore": 88, "skills": ["Python", "SQL", "数据分析", "Excel"], "experience": "应届", "degree": "本科"},
            {"id": 6, "title": "测试工程师", "company": "京东", "location": "北京", "salary": "12-20K", "industry": "电商", "matchScore": 83, "skills": ["测试用例", "自动化测试", "缺陷管理", "Linux"], "experience": "应届", "degree": "本科"},
            {"id": 7, "title": "Go后端开发", "company": "字节跳动", "location": "上海", "salary": "17-32K", "industry": "互联网", "matchScore": 89, "skills": ["Go", "gRPC", "Kubernetes", "Docker"], "experience": "应届", "degree": "本科"},
            {"id": 8, "title": "iOS开发工程师", "company": "腾讯", "location": "深圳", "salary": "16-30K", "industry": "互联网", "matchScore": 86, "skills": ["Swift", "Objective-C", "iOS SDK", "Xcode"], "experience": "应届", "degree": "本科"},
            {"id": 9, "title": "Android开发工程师", "company": "阿里巴巴", "location": "杭州", "salary": "15-28K", "industry": "电商", "matchScore": 84, "skills": ["Java", "Kotlin", "Android SDK", "Jetpack"], "experience": "应届", "degree": "本科"},
            {"id": 10, "title": "数据工程师", "company": "美团", "location": "北京", "salary": "16-28K", "industry": "本地生活", "matchScore": 87, "skills": ["Python", "Spark", "Hadoop", "Hive"], "experience": "应届", "degree": "本科"},
            {"id": 11, "title": "运维工程师", "company": "华为", "location": "深圳", "salary": "14-26K", "industry": "通信", "matchScore": 82, "skills": ["Linux", "Shell", "Ansible", "Prometheus"], "experience": "应届", "degree": "本科"},
            {"id": 12, "title": "安全工程师", "company": "奇安信", "location": "北京", "salary": "15-30K", "industry": "安全", "matchScore": 85, "skills": ["渗透测试", "漏洞分析", "安全审计", "Linux"], "experience": "应届", "degree": "本科"},
            {"id": 13, "title": "云计算工程师", "company": "阿里云", "location": "杭州", "salary": "18-35K", "industry": "云计算", "matchScore": 88, "skills": ["AWS", "Docker", "Kubernetes", "Terraform"], "experience": "应届", "degree": "本科"},
            {"id": 14, "title": "嵌入式开发", "company": "小米", "location": "北京", "salary": "14-26K", "industry": "硬件", "matchScore": 83, "skills": ["C/C++", "RTOS", "ARM", "Linux"], "experience": "应届", "degree": "本科"},
            {"id": 15, "title": "UI设计师", "company": "网易", "location": "杭州", "salary": "12-22K", "industry": "互联网", "matchScore": 80, "skills": ["Figma", "Sketch", "Photoshop", "交互设计"], "experience": "应届", "degree": "本科"},
            {"id": 16, "title": "后端开发", "company": "拼多多", "location": "上海", "salary": "17-32K", "industry": "电商", "matchScore": 86, "skills": ["Python", "Flask", "MySQL", "Redis"], "experience": "应届", "degree": "本科"},
            {"id": 17, "title": "游戏开发", "company": "网易", "location": "广州", "salary": "16-30K", "industry": "游戏", "matchScore": 85, "skills": ["C++", "Unity", "Unreal", "游戏引擎"], "experience": "应届", "degree": "本科"},
            {"id": 18, "title": "技术运营", "company": "小红书", "location": "上海", "salary": "12-20K", "industry": "互联网", "matchScore": 78, "skills": ["数据分析", "SQL", "运营策略", "沟通协调"], "experience": "应届", "degree": "本科"},
            {"id": 19, "title": "研发工程师", "company": "华为", "location": "西安", "salary": "15-28K", "industry": "通信", "matchScore": 84, "skills": ["C/C++", "Java", "数据结构", "算法"], "experience": "应届", "degree": "硕士"},
            {"id": 20, "title": "软件工程师", "company": "微软", "location": "上海", "salary": "20-40K", "industry": "外企", "matchScore": 91, "skills": ["C#", ".NET", "Azure", "SQL Server"], "experience": "应届", "degree": "硕士"},
        ],
        "resume_example": {
            "name": "张三",
            "gender": "男",
            "phone": "13800138000",
            "email": "zhangsan@example.com",
            "degree": "本科",
            "graduationTime": "2025-06",
            "skills": ["Java", "Python", "SQL", "Spring Boot", "React", "JavaScript"],
            "education": [{"school": "清华大学", "major": "计算机科学", "startDate": "2021-09", "endDate": "2025-06", "degree": "本科"}],
            "experience": [{"company": "字节跳动", "position": "前端开发实习生", "startDate": "2024-06", "endDate": "2024-09", "description": "参与抖音Web端开发，负责多个页面的前端实现"}],
        },
        "optimizations": [
            {"id": 1, "priority": "高", "title": "项目经验描述不够详细", "suggestion": "建议使用STAR法则描述项目经验，突出自己的贡献和成果", "original": "参与了一个电商网站的开发", "optimized": "作为核心开发者参与电商网站前端开发，负责用户模块和订单模块，使用React+TypeScript技术栈，优化了页面加载速度30%"},
            {"id": 2, "priority": "中", "title": "技能标签需要优化", "suggestion": "增加更多与目标岗位相关的技能标签，如Redis、消息队列等", "original": "熟练使用Java", "optimized": "熟练使用Java、Spring Boot、MySQL、Redis、RabbitMQ"},
            {"id": 3, "priority": "低", "title": "个人评价过于笼统", "suggestion": "加入具体的个人优势和职业规划", "original": "本人学习能力强，团队合作意识好", "optimized": "拥有扎实的计算机基础，对新技术有强烈的好奇心，善于团队协作，目标是成为一名优秀的全栈工程师"},
        ]
    }

def save_data(data):
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"数据保存失败: {str(e)}")
        return False

app_data = load_data()

if 'favorites' not in st.session_state:
    st.session_state.favorites = []

if 'resume_data' not in st.session_state:
    st.session_state.resume_data = None

if 'current_page' not in st.session_state:
    st.session_state.current_page = "home"

if 'jobs' not in st.session_state:
    st.session_state.jobs = app_data["jobs"]

MOCK_JOBS = app_data["jobs"]
MOCK_RESUME = app_data["resume_example"]
MOCK_OPTIMIZATIONS = app_data["optimizations"]
STATS_DATA = app_data["stats"]

def call_api(endpoint, method="GET", data=None):
    try:
        url = f"{API_URL}/{endpoint}"
        if method == "GET":
            response = requests.get(url)
        else:
            response = requests.post(url, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            return {"success": False, "error": f"API请求失败: {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"无法连接到后端服务: {str(e)}"}

def toggle_favorite(job_id):
    if job_id in st.session_state.favorites:
        st.session_state.favorites.remove(job_id)
    else:
        st.session_state.favorites.append(job_id)

def navigate_to(page_name, view_mode=None):
    st.session_state.current_page = page_name
    if view_mode:
        st.session_state.view_mode = view_mode

def update_stats_data(new_stats):
    app_data["stats"] = new_stats
    if save_data(app_data):
        global STATS_DATA
        STATS_DATA = new_stats

def parse_salary(salary_str):
    try:
        if not salary_str or not isinstance(salary_str, str):
            return 0, 100
        salary_str = salary_str.replace('K', '').replace('k', '')
        if '-' in salary_str:
            parts = salary_str.split('-')
            return int(parts[0]), int(parts[1])
        return int(salary_str), int(salary_str)
    except:
        return 0, 100

def home_page():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e40af 0%, #3b82f6 50%, #60a5fa 100%); padding: 40px; border-radius: 16px;">
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 16px;">
            <span style="background: rgba(255,255,255,0.2); padding: 4px 12px; border-radius: 20px; font-size: 12px; color: white;">
                🤖 AI智能驱动 · 校招专属
            </span>
        </div>
        <h1 style="color: white; font-size: 36px; font-weight: bold; margin-bottom: 16px;">
            校招岗位智能匹配系统
        </h1>
        <div style="display: flex; gap: 24px; margin-bottom: 24px;">
            <span style="color: rgba(255,255,255,0.9); font-size: 14px;">
                📄 一键解析简历
            </span>
            <span style="color: rgba(255,255,255,0.9); font-size: 14px;">
                🎯 智能匹配岗位
            </span>
            <span style="color: rgba(255,255,255,0.9); font-size: 14px;">
                📊 科学规划求职
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.button("📤 立即上传简历", key="hero_resume", use_container_width=True, on_click=navigate_to, args=("resume",))
    
    with col2:
        st.button("查看岗位推荐 →", key="hero_match", use_container_width=True, on_click=navigate_to, args=("match",))
    
    st.write("")
    
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    stats_result = call_api("stats")
    if stats_result.get("success"):
        stats_data = stats_result["data"]
    else:
        stats_data = STATS_DATA
    
    with stat_col1:
        st.markdown(f"""
        <div style="background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="background: #dbeafe; padding: 10px; border-radius: 10px;">
                    <span style="font-size: 20px;">💼</span>
                </div>
                <div>
                    <div style="color: #64748b; font-size: 12px;">收录岗位</div>
                    <div style="color: #1e293b; font-size: 20px; font-weight: bold;">{stats_data.get('total_jobs', 0)} 个</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with stat_col2:
        st.markdown(f"""
        <div style="background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="background: #d1fae5; padding: 10px; border-radius: 10px;">
                    <span style="font-size: 20px;">👥</span>
                </div>
                <div>
                    <div style="color: #64748b; font-size: 12px;">服务学生</div>
                    <div style="color: #1e293b; font-size: 20px; font-weight: bold;">{stats_data.get('total_students', 0)}+</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with stat_col3:
        st.markdown(f"""
        <div style="background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="background: #fef3c7; padding: 10px; border-radius: 10px;">
                    <span style="font-size: 20px;">⭐</span>
                </div>
                <div>
                    <div style="color: #64748b; font-size: 12px;">平均匹配度</div>
                    <div style="color: #1e293b; font-size: 20px; font-weight: bold;">{stats_data.get('avg_match_rate', 0)}%</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with stat_col4:
        st.markdown(f"""
        <div style="background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="background: #cffafe; padding: 10px; border-radius: 10px;">
                    <span style="font-size: 20px;">⚡</span>
                </div>
                <div>
                    <div style="color: #64748b; font-size: 12px;">解析耗时</div>
                    <div style="color: #1e293b; font-size: 20px; font-weight: bold;">{stats_data.get('parse_time', '<5秒')}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.write("")
    st.markdown("<h2 style='color: #1e293b; font-size: 18px; font-weight: bold;'>核心功能</h2>", unsafe_allow_html=True)
    
    func_col1, func_col2, func_col3, func_col4 = st.columns(4)
    
    with func_col1:
        st.markdown("""
        <div style="background: white; padding: 24px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
            <div style="background: #dbeafe; padding: 12px; border-radius: 12px; width: fit-content; margin-bottom: 16px;">
                <span style="font-size: 24px;">📤</span>
            </div>
            <h3 style="color: #1e293b; font-size: 16px; font-weight: bold; margin-bottom: 8px;">简历上传与解析</h3>
            <p style="color: #64748b; font-size: 13px; line-height: 1.5; margin-bottom: 16px;">支持PDF/Word简历，自动提取姓名、学历、技能、实习等关键信息</p>
        </div>
        """, unsafe_allow_html=True)
        st.button("进入功能 →", key="func_resume", use_container_width=True, on_click=navigate_to, args=("resume",))
    
    with func_col2:
        st.markdown("""
        <div style="background: white; padding: 24px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
            <div style="background: #d1fae5; padding: 12px; border-radius: 12px; width: fit-content; margin-bottom: 16px;">
                <span style="font-size: 24px;">🎯</span>
            </div>
            <h3 style="color: #1e293b; font-size: 16px; font-weight: bold; margin-bottom: 8px;">智能岗位匹配</h3>
            <p style="color: #64748b; font-size: 13px; line-height: 1.5; margin-bottom: 16px;">基于简历标签智能匹配校招岗位，匹配度可视化，优先推荐高分岗位</p>
        </div>
        """, unsafe_allow_html=True)
        st.button("进入功能 →", key="func_match", use_container_width=True, on_click=navigate_to, args=("match",))
    
    with func_col3:
        st.markdown("""
        <div style="background: white; padding: 24px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
            <div style="background: #fce7f3; padding: 12px; border-radius: 12px; width: fit-content; margin-bottom: 16px;">
                <span style="font-size: 24px;">✏️</span>
            </div>
            <h3 style="color: #1e293b; font-size: 16px; font-weight: bold; margin-bottom: 8px;">简历优化建议</h3>
            <p style="color: #64748b; font-size: 13px; line-height: 1.5; margin-bottom: 16px;">针对目标岗位生成可落地的优化建议，高亮薄弱点，一键复制优化文案</p>
        </div>
        """, unsafe_allow_html=True)
        st.button("进入功能 →", key="func_optimize", use_container_width=True, on_click=navigate_to, args=("optimize",))
    
    with func_col4:
        st.markdown("""
        <div style="background: white; padding: 24px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
            <div style="background: #fef3c7; padding: 12px; border-radius: 12px; width: fit-content; margin-bottom: 16px;">
                <span style="font-size: 24px;">📊</span>
            </div>
            <h3 style="color: #1e293b; font-size: 16px; font-weight: bold; margin-bottom: 8px;">求职数据统计</h3>
            <p style="color: #64748b; font-size: 13px; line-height: 1.5; margin-bottom: 16px;">行业薪资分布、岗位需求热度、个人能力雷达，科学规划求职路线</p>
        </div>
        """, unsafe_allow_html=True)
        st.button("进入功能 →", key="func_stats", use_container_width=True, on_click=navigate_to, args=("stats",))
    
    st.write("")
    st.markdown("<h2 style='color: #1e293b; font-size: 18px; font-weight: bold;'>使用流程</h2>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background: white; padding: 32px; border-radius: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 0;">
            <div style="display: flex; flex-direction: column; align-items: center; text-align: center; padding: 0 20px;">
                <div style="background: #2563eb; padding: 16px; border-radius: 16px; margin-bottom: 16px;">
                    <span style="font-size: 28px;">📄</span>
                </div>
                <div style="color: #2563eb; font-size: 12px; font-weight: bold; margin-bottom: 8px;">01 上传简历</div>
                <p style="color: #64748b; font-size: 13px; line-height: 1.5;">拖拽或点击上传 PDF/Word 格式简历，系统自动解析提取信息</p>
            </div>
            <div style="display: flex; flex-direction: column; align-items: center; text-align: center; padding: 0 20px; border-left: 2px solid #e2e8f0; border-right: 2px solid #e2e8f0;">
                <div style="background: #2563eb; padding: 16px; border-radius: 16px; margin-bottom: 16px;">
                    <span style="font-size: 28px;">🎯</span>
                </div>
                <div style="color: #2563eb; font-size: 12px; font-weight: bold; margin-bottom: 8px;">02 选择岗位</div>
                <p style="color: #64748b; font-size: 13px; line-height: 1.5;">设置目标城市、行业、薪资偏好，一键生成智能匹配结果</p>
            </div>
            <div style="display: flex; flex-direction: column; align-items: center; text-align: center; padding: 0 20px;">
                <div style="background: #2563eb; padding: 16px; border-radius: 16px; margin-bottom: 16px;">
                    <span style="font-size: 28px;">📈</span>
                </div>
                <div style="color: #2563eb; font-size: 12px; font-weight: bold; margin-bottom: 8px;">03 优化求职</div>
                <p style="color: #64748b; font-size: 13px; line-height: 1.5;">获取个性化简历优化建议，参考求职数据分析，提升竞争力</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    cta_col1, cta_col2 = st.columns([4, 1])
    with cta_col1:
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="background: #2563eb; padding: 8px; border-radius: 10px;">
                <span style="font-size: 16px;">✅</span>
            </div>
            <div>
                <div style="color: #1e293b; font-size: 16px; font-weight: bold;">准备好了吗？</div>
                <p style="color: #64748b; font-size: 13px;">上传你的简历，让 AI 为你匹配最适合的校招岗位，提升求职成功率</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with cta_col2:
        st.button("开始体验", key="cta_button", use_container_width=True, on_click=navigate_to, args=("resume",))

def resume_page():
    st.title("简历上传解析 📤")
    st.write("选择简历文件")
    uploaded_file = st.file_uploader("", type=["pdf", "docx", "txt"], label_visibility="collapsed")
    
    # 手动输入简历文本的选项
    st.write("或者手动输入简历内容：")
    resume_text = st.text_area("简历内容", height=200)
    
    if uploaded_file is not None:
        with st.spinner("正在解析简历，请稍候..."):
            try:
                file_content = uploaded_file.read().decode('utf-8', errors='ignore')
                result = call_api("parse_resume", method="POST", data={"resume": file_content})
                
                if result.get("success"):
                    st.session_state.resume_data = result["data"]
                    st.success("简历解析完成！")
                    st.success("简历解析完成！")
                else:
                    st.warning(f"解析失败，使用示例数据: {result.get('error', '未知错误')}")
                    st.session_state.resume_data = MOCK_RESUME
            except Exception as e:
                st.warning(f"文件读取失败，使用示例数据: {str(e)}")
                st.session_state.resume_data = MOCK_RESUME
    
    elif resume_text.strip():
        with st.spinner("正在解析简历，请稍候..."):
            result = call_api("parse_resume", method="POST", data={"resume": resume_text})
            
            if result.get("success"):
                st.session_state.resume_data = result["data"]
                st.success("简历解析完成！")
                st.success("简历解析完成！")
            else:
                st.warning(f"解析失败，使用示例数据: {result.get('error', '未知错误')}")
                st.session_state.resume_data = MOCK_RESUME
    
    if st.session_state.resume_data or st.checkbox("使用示例数据"):
        resume = st.session_state.resume_data if st.session_state.resume_data else MOCK_RESUME
        
        st.markdown("---")
        st.subheader("个人信息")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"**姓名**: {resume.get('name', '未知')}")
            st.write(f"**性别**: {resume.get('gender', '未知')}")
        with col2:
            st.write(f"**电话**: {resume.get('phone', '未知')}")
            st.write(f"**邮箱**: {resume.get('email', '未知')}")
        with col3:
            st.write(f"**学历**: {resume.get('degree', '未知')}")
            st.write(f"**毕业时间**: {resume.get('graduationTime', '未知')}")
        
        st.subheader("技能标签")
        skills = resume.get('skills', [])
        if skills:
            st.write(", ".join([f"🏷️ {s}" for s in skills]))
        else:
            st.info("暂无技能信息")
        
        st.subheader("教育背景")
        education = resume.get('education', [])
        if education:
            for edu in education:
                st.write(f"🎓 **{edu.get('school', '未知学校')}** - {edu.get('major', '未知专业')} ({edu.get('startDate', '未知')} ~ {edu.get('endDate', '未知')})")
        else:
            st.info("暂无教育背景信息")
        
        st.subheader("实习经历")
        experience = resume.get('experience', [])
        if experience:
            for exp in experience:
                st.write(f"💼 **{exp.get('company', '未知公司')}** - {exp.get('position', '未知职位')} ({exp.get('startDate', '未知')} ~ {exp.get('endDate', '未知')})")
                st.write(f"   {exp.get('description', '暂无描述')}")
        else:
            st.info("暂无实习经历信息")

def match_page():
    st.title("智能岗位匹配 🎯")
    
    default_view = "我的收藏" if st.session_state.get("view_mode") == "favorites" else "全部岗位"
    view_mode = st.radio("查看模式", ["全部岗位", "我的收藏"], horizontal=True, index=["全部岗位", "我的收藏"].index(default_view))
    
    if st.session_state.get("view_mode"):
        del st.session_state["view_mode"]
    
    if view_mode == "我的收藏":
        if not st.session_state.favorites:
            st.info("您还没有收藏任何岗位")
            return
        jobs = [job for job in st.session_state.jobs if job['id'] in st.session_state.favorites]
    else:
        jobs = st.session_state.jobs
    
    search_keyword = st.text_input("关键词搜索", "")
    
    locations = ["全部"] + sorted(list(set([job.get('location', '未知') for job in st.session_state.jobs])))
    industries = ["全部"] + sorted(list(set([job.get('industry', '未知') for job in st.session_state.jobs])))
    
    col1, col2, col3 = st.columns(3)
    with col1:
        location_filter = st.selectbox("城市筛选", locations)
    with col2:
        industry_filter = st.selectbox("行业筛选", industries)
    with col3:
        salary_range = st.slider("薪资范围 (K)", 10, 40, (10, 40))
    
    degree_filter = st.selectbox("学历要求", ["全部", "本科", "硕士", "博士"])
    experience_filter = st.selectbox("经验要求", ["全部", "应届", "1-3年", "3-5年"])
    sort_by = st.selectbox("排序方式", ["匹配度", "薪资", "热度"])
    
    filtered_jobs = jobs
    if search_keyword:
        filtered_jobs = [job for job in filtered_jobs 
                        if search_keyword.lower() in job.get('title', '').lower() 
                        or search_keyword.lower() in job.get('company', '').lower()]
    if location_filter != "全部":
        filtered_jobs = [job for job in filtered_jobs if job.get('location') == location_filter]
    if industry_filter != "全部":
        filtered_jobs = [job for job in filtered_jobs if job.get('industry') == industry_filter]
    
    filtered_jobs = [job for job in filtered_jobs 
                    if parse_salary(job.get('salary', '0-0K'))[0] >= salary_range[0] 
                    and parse_salary(job.get('salary', '0-0K'))[1] <= salary_range[1]]
    
    if degree_filter != "全部":
        filtered_jobs = [job for job in filtered_jobs if job.get('degree') == degree_filter]
    if experience_filter != "全部":
        filtered_jobs = [job for job in filtered_jobs if job.get('experience') == experience_filter]
    
    if sort_by == "匹配度":
        filtered_jobs = sorted(filtered_jobs, key=lambda x: x.get('matchScore', 0), reverse=True)
    elif sort_by == "薪资":
        filtered_jobs = sorted(filtered_jobs, key=lambda x: parse_salary(x.get('salary', '0K'))[1], reverse=True)
    
    if not filtered_jobs:
        st.info("没有找到符合条件的岗位，请尝试调整筛选条件")
        return
    
    st.write(f"共找到 **{len(filtered_jobs)}** 个岗位")
    
    for job in filtered_jobs:
        is_fav = job['id'] in st.session_state.favorites
        col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
        with col1:
            st.markdown(f"**{job.get('title', '未知岗位')}**")
            st.write(f"🏢 {job.get('company', '未知公司')} | 🏢 {job.get('industry', '未知行业')}")
        with col2:
            st.write(f"💰 {job.get('salary', '未知薪资')}")
        with col3:
            st.write(f"📍 {job.get('location', '未知地点')}")
        with col4:
            st.write(f"📊 {job.get('matchScore', 0)}%")
            st.progress(job.get('matchScore', 0) / 100)
        with col5:
            st.button("❤️" if is_fav else "🤍", key=f"match_fav_{job['id']}", on_click=toggle_favorite, args=(job['id'],))

def optimize_page():
    st.title("简历优化建议 ✏️")
    
    if not st.session_state.resume_data:
        st.warning("请先上传简历以获取个性化优化建议")
        st.button("去上传简历", key="go_resume", on_click=navigate_to, args=("resume",))
        return
    
    st.markdown("---")
    
    resume_text = json.dumps(st.session_state.resume_data)
    result = call_api("optimize_resume", method="POST", data={"resume": resume_text})
    
    if result.get("success"):
        optimizations = result["data"]
    else:
        st.warning(f"获取优化建议失败，使用示例数据: {result.get('error', '未知错误')}")
        optimizations = MOCK_OPTIMIZATIONS
    
    if not optimizations:
        st.info("暂无优化建议，请先上传简历")
        return
    
    for i, opt in enumerate(optimizations):
        priority_color = {"高": "#ef4444", "中": "#f59e0b", "低": "#10b981"}.get(opt.get('priority', '中'), "#94a3b8")
        st.markdown(f"""
        <div style="background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); margin-bottom: 16px;">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
                <span style="background: {priority_color}; color: white; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold;">
                    {opt.get('priority', '中')}优先级
                </span>
                <h3 style="color: #1e293b; font-size: 16px; font-weight: bold;">{opt.get('title', '优化建议')}</h3>
            </div>
            <p style="color: #64748b; font-size: 14px; margin-bottom: 12px;">💡 {opt.get('suggestion', '暂无建议')}</p>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                <div style="background: #f8fafc; padding: 12px; border-radius: 8px;">
                    <div style="color: #94a3b8; font-size: 12px; margin-bottom: 4px;">原句</div>
                    <div style="color: #64748b; font-size: 13px;">{opt.get('original', '暂无')}</div>
                </div>
                <div style="background: #ecfdf5; padding: 12px; border-radius: 8px;">
                    <div style="color: #059669; font-size: 12px; margin-bottom: 4px;">优化后</div>
                    <div style="color: #065f46; font-size: 13px;">{opt.get('optimized', '暂无')}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.button(f"📋 复制优化文案", key=f"copy_opt_{i}")
    
    st.write("")
    st.markdown("---")
    
    if st.button("📄 导出优化后的简历", key="export_resume"):
        st.success("简历导出成功！已保存到 app_data.json 文件中")
        st.info("与算法工程师对接后，可实现真正的导出功能")

def stats_page():
    st.title("求职数据统计 📊")
    
    st.subheader("行业薪资分布")
    salary_data = {
        "互联网": {"平均": 18, "最高": 35, "最低": 12},
        "电商": {"平均": 16, "最高": 30, "最低": 10},
        "AI": {"平均": 22, "最高": 40, "最低": 15},
        "金融": {"平均": 17, "最高": 32, "最低": 11},
    }
    
    st.table(salary_data)
    
    st.subheader("个人能力雷达")
    skills = ["Java", "Python", "SQL", "前端", "算法"]
    scores = [85, 75, 90, 60, 70]
    
    for i, skill in enumerate(skills):
        st.write(f"**{skill}**: {scores[i]}%")
        st.progress(scores[i] / 100)
    
    st.subheader("求职趋势")
    trend_data = {
        "日期": ["1月", "2月", "3月", "4月", "5月", "6月"],
        "投递数量": [15, 20, 25, 30, 35, 40],
        "面试邀请": [5, 8, 10, 12, 15, 18],
    }
    
    st.line_chart(trend_data, x="日期")
    
    st.subheader("热门岗位排行")
    if st.session_state.jobs:
        sorted_jobs = sorted(st.session_state.jobs, key=lambda x: x.get('matchScore', 0), reverse=True)
        for i, job in enumerate(sorted_jobs[:5], 1):
            st.write(f"{i}. **{job.get('title', '未知岗位')}** - {job.get('company', '未知公司')} ({job.get('matchScore', 0)}%匹配度)")

def data_management_page():
    st.title("数据管理 🛠️")
    
    st.subheader("更新统计数据")
    
    col1, col2 = st.columns(2)
    with col1:
        new_total_jobs = st.number_input("收录岗位数量", min_value=0, value=STATS_DATA.get('total_jobs', 0))
        new_total_students = st.number_input("服务学生数量", min_value=0, value=STATS_DATA.get('total_students', 0))
    with col2:
        new_avg_match_rate = st.number_input("平均匹配度 (%)", min_value=0.0, max_value=100.0, value=STATS_DATA.get('avg_match_rate', 0.0))
        new_parse_time = st.text_input("解析耗时", value=STATS_DATA.get('parse_time', '<5秒'))
    
    if st.button("💾 保存统计数据", use_container_width=True):
        try:
            new_stats = {
                "total_jobs": int(new_total_jobs),
                "total_students": int(new_total_students),
                "avg_match_rate": float(new_avg_match_rate),
                "parse_time": str(new_parse_time)
            }
            update_stats_data(new_stats)
            st.success("数据更新成功！")
            st.success("数据更新成功！")
        except Exception as e:
            st.error(f"数据保存失败: {str(e)}")
            st.error(f"数据保存失败: {str(e)}")
    
    st.markdown("---")
    st.subheader("数据操作")
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "📥 导出当前数据",
            data=json.dumps(app_data, ensure_ascii=False, indent=2),
            file_name="app_data.json",
            mime="application/json",
            use_container_width=True
        )
    with col2:
        if st.button("🔄 恢复默认数据", use_container_width=True):
            if save_data(get_default_data()):
                st.session_state.reset_data = True
                st.info("已恢复默认数据！请刷新页面")
                st.success("已恢复默认数据！请刷新页面以应用更改")
    
    st.markdown("---")
    st.subheader("数据统计")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("岗位数量", len(st.session_state.jobs))
    with col2:
        st.metric("优化建议数", len(app_data.get("optimizations", [])))
    with col3:
        st.metric("收藏岗位", len(st.session_state.favorites))
    
    st.markdown("---")
    st.subheader("数据文件信息")
    st.write(f"数据存储在: `{os.path.abspath(DATA_FILE)}`")
    
    if os.path.exists(DATA_FILE):
        file_size = os.path.getsize(DATA_FILE)
        st.info(f"文件大小: {file_size} 字节")
    else:
        st.warning("数据文件不存在")
    
    st.markdown("---")
    st.subheader("批量导入数据")
    uploaded_json = st.file_uploader("上传 JSON 数据文件", type=["json"])
    if uploaded_json is not None:
        try:
            imported_data = json.load(uploaded_json)
            validated_data = validate_data(imported_data)
            if save_data(validated_data):
                st.success("数据导入成功！")
                st.success("数据导入成功！请刷新页面以应用更改")
        except Exception as e:
            st.error(f"数据格式错误: {str(e)}")
            st.error(f"数据格式错误，请检查 JSON 文件")

# 初始化岗位数据
if 'jobs_initialized' not in st.session_state:
    jobs_result = call_api("jobs")
    if jobs_result.get("success"):
        st.session_state.jobs = jobs_result["data"]
    else:
        st.session_state.jobs = MOCK_JOBS
    st.session_state.jobs_initialized = True

fav_count = len(st.session_state.favorites)
resume_count = 1 if st.session_state.resume_data else 0

st.sidebar.markdown("""
<style>
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #162d4a 0%, #0f1f35 100%);
    }
    [data-testid="stSidebar"] .stButton>button {
        width: 100%;
        background: transparent;
        color: #cbd5e1;
        border: none;
        text-align: left;
        padding: 12px 16px;
        margin-bottom: 4px;
        border-radius: 8px;
        transition: all 0.2s;
    }
    [data-testid="stSidebar"] .stButton>button:hover {
        background: rgba(255,255,255,0.1);
    }
    [data-testid="stSidebar"] .stButton>button:disabled {
        background: #3b82f6;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px; padding-top: 20px;">
    <div style="background: #2563eb; padding: 12px; border-radius: 12px;">
        <span style="font-size: 24px;">💼</span>
    </div>
    <div>
        <div style="color: white; font-size: 16px; font-weight: bold;">校招智配</div>
        <div style="color: #93c5fd; font-size: 12px;">智能求职助手</div>
    </div>
</div>
<div style="color: #93c5fd; font-size: 12px; margin-bottom: 24px;">一键解析简历 · 智能匹配岗位 · 科学规划求职</div>
""", unsafe_allow_html=True)

st.sidebar.write("")
st.sidebar.markdown("<span style='color: white; font-weight: bold;'>功能导航</span>", unsafe_allow_html=True)
st.sidebar.button("🏠 首页", key="nav_home", use_container_width=True, on_click=navigate_to, args=("home",), disabled=st.session_state.current_page == "home")
st.sidebar.button("📤 简历上传解析", key="nav_resume", use_container_width=True, on_click=navigate_to, args=("resume",), disabled=st.session_state.current_page == "resume")
st.sidebar.button("🎯 智能岗位匹配", key="nav_match", use_container_width=True, on_click=navigate_to, args=("match",), disabled=st.session_state.current_page == "match")
st.sidebar.button("✏️ 简历优化建议", key="nav_optimize", use_container_width=True, on_click=navigate_to, args=("optimize",), disabled=st.session_state.current_page == "optimize")
st.sidebar.button("📊 求职数据统计", key="nav_stats", use_container_width=True, on_click=navigate_to, args=("stats",), disabled=st.session_state.current_page == "stats")
st.sidebar.button("🛠️ 数据管理", key="nav_data", use_container_width=True, on_click=navigate_to, args=("data_management",), disabled=st.session_state.current_page == "data_management")

st.sidebar.write("")
st.sidebar.markdown("<span style='color: white; font-weight: bold;'>快捷入口</span>", unsafe_allow_html=True)
st.sidebar.button(f"⭐ 收藏岗位 ({fav_count})", key="nav_favorites", use_container_width=True, on_click=navigate_to, args=("match", "favorites"))

st.sidebar.write("")
st.sidebar.markdown("""
<div style="background: #1e3a5f; padding: 16px; border-radius: 12px;">
    <div style="color: #93c5fd; font-size: 12px; margin-bottom: 12px;">系统状态</div>
    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
        <span style="color: #cbd5e1; font-size: 14px;">已解析简历</span>
        <span style="color: white; font-size: 16px; font-weight: bold;">""" + str(len(st.session_state.get('resume_history', [])) + (1 if st.session_state.resume_data else 0)) + """ 份</span>
    </div>
    <div style="display: flex; justify-content: space-between;">
        <span style="color: #cbd5e1; font-size: 14px;">收藏岗位</span>
        <span style="color: white; font-size: 16px; font-weight: bold;">""" + str(fav_count) + """ 个</span>
    </div>
</div>
""", unsafe_allow_html=True)

if st.session_state.current_page == "home":
    home_page()
elif st.session_state.current_page == "resume":
    resume_page()
elif st.session_state.current_page == "match":
    match_page()
elif st.session_state.current_page == "optimize":
    optimize_page()
elif st.session_state.current_page == "stats":
    stats_page()
elif st.session_state.current_page == "data_management":
    data_management_page()
else:
    home_page()
