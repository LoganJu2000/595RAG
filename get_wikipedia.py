import requests
from bs4 import BeautifulSoup


def get_wikipedia_page(query):
    """
    获取与查询最相关的 Wikipedia 页面内容
    """
    # 搜索 Wikipedia API
    search_url = "https://en.wikipedia.org/w/api.php"
    search_params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json",
    }

    response = requests.get(search_url, params=search_params)
    if response.status_code != 200:
        print("搜索请求失败！")
        return None

    search_results = response.json()
    if not search_results["query"]["search"]:
        print("没有找到相关结果！")
        return None

    # 获取第一个结果的标题
    page_title = search_results["query"]["search"][0]["title"]
    # print(len(search_results["query"]["search"]))
    # print("this is result:", search_results["query"]["search"])
    print(f"找到的页面标题: {page_title}")

    # 获取页面内容
    page_url = f"https://en.wikipedia.org/wiki/{page_title.replace(' ', '_')}"
    page_response = requests.get(page_url)
    if page_response.status_code != 200:
        print("获取页面内容失败！")
        return None

    soup = BeautifulSoup(page_response.text, "html.parser")
    content = soup.find("div", {"id": "mw-content-text"})
    if not content:
        print("未找到页面内容！")
        return None

    # 提取纯文本内容
    paragraphs = content.find_all("p")
    page_content = "\n".join([p.get_text() for p in paragraphs if p.get_text().strip()])

    return page_title, page_url, page_content


if __name__ == "__main__":
    query = input("请输入查询词: ")
    result = get_wikipedia_page(query)
    if result:
        title, url, content = result
        print(f"\n页面标题: {title}")
        print(f"页面链接: {url}")
        print(f"\n页面内容预览:\n{content[:1000]}...")  # 只显示前1000个字符
