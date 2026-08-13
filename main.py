# from sites.parser import Parser
# from sites.config_loader import load_config_for_url   
from core.processmanager import ProcessManager
from core.logging_config import setup_logging

if __name__ == "__main__":
    setup_logging()
    url = 'https://m.shuhaige.net/382358/'
    # url = "https://www.cnblogs.com/HarmonyOSSDK/p/21237380"
    # url = "https://cn-sec.com/archives/5387823.html"
    url = "https://cn-sec.com/archives/category/安全文章"
    url = "https://cn-sec.com/archives/category/安全文章/人工智能安全"
    manager = ProcessManager(url)
    manager.run()
