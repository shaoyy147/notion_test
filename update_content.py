# %%
from notion_client import Client
from typing import List, Tuple
from textwrap import dedent
from datetime import datetime

import os

# %%
auth = os.environ.get("NOTION_AUTH")
notion_database_id = os.environ.get("NOTION_DATABASE_ID")

# %%
notion = Client(auth=auth)
FILTER = {
    "property": "Publish",
    "select": {
        "equals": "Yes"
    }
}
notion_pages = notion.databases.query(notion_database_id, filter=FILTER)['results']
print(f"total num of pages: {len(notion_pages)}")


# %%
TIME_FORMAT = r'%Y-%m-%dT%H:%M:%S.000%z'
class MomentPage:
    def __init__(self, raw_page_meta_info: dict) -> None:
        self.raw_page_meta_info: dict = raw_page_meta_info


        self.output: List[Tuple[str, str]]= []

        self.page_id: str = None,
        self.page_name: str = None,
        self.created_time: datetime = None,

        self.author: str = None,
        self.signature: str = None,

        self.tags: List[str] = None,

        self.note: str = "", 
        self.resource: str = None


    def parse(self):
        notion_database_page = self.raw_page_meta_info

        # -- parse meta info -- 
        self.page_id = notion_database_page['id']
        self.name = "".join(rich_text_part['plain_text'] for rich_text_part in notion_database_page['properties']['Name']['title'])
        self.signature = "".join(rich_text_part['plain_text'] for rich_text_part in notion_database_page['properties']['Signature']['rich_text'])

        if notion_database_page['properties']['Date']['date']:
            self.created_time = datetime.strptime(notion_database_page['properties']['Date']['date']['start'], TIME_FORMAT)
        else:
            self.created_time = datetime.strptime(notion_database_page['created_time'], TIME_FORMAT)

        self.tags = [tag['name'] for tag in notion_database_page['properties']['Tags']['multi_select']]

        if "Note" in notion_database_page['properties']:
            self.note = "".join(rich_text_part['plain_text'] for rich_text_part in notion_database_page['properties']['Note']['rich_text'])

        # todo
        # author = moment_page['properties']['Author']
        self.author = None

        # todo is_top

        # -- parse content blocks -0
        page_blocks = notion.blocks.children.list(notion_database_page['id'])
        self._parse_notion_blocks(page_blocks['results'])

    
    def to_hugo_md_page_str(self) -> str:
        _tag_part = "\n".join(f"  - {tag}" for tag in self.tags)
        _pictures_part = "\n".join(f"  - {text}" for text_type, text in self.output if text_type == "img")
        yaml_part = dedent(
            f"""
                ---
                top:
                name: {self.author if self.author else ""}
                avatar:
                signature: {self.signature if self.signature else ""}

                date: {self.created_time.strftime(r'%Y-%m-%dT%H:%M:%S%z')[:-2] + ":00"}

                tags:
                {{tag_part}}

                pictures:
                {{picture_part}}

                link: {self.resource if self.resource else ""}
                link_logo:
                link_text: 

                note: {self.note}
                ---
            """
        )  \
        .strip(" \n") \
        .format(tag_part=_tag_part, picture_part=_pictures_part)

        return yaml_part + "\n" + self._return_md_context()


    def _return_md_context(self) -> str:
        return "\n\n".join(text for text_type, text in self.output if text_type != "img")


    def _parse_notion_blocks(self, blocks: List[dict]):
        for block in blocks: self._parse_block(block)


    def _parse_block(self, block):
        if block['type'] == "paragraph": self._parse_paragraph(block=block)
        if block['type'] == "image": self._parse_image(block=block)
        if block['type'] == "code": self._parse_code(block=block)
        if block['type'] == "quote": self._parse_quote(block=block)

        # todo
        # bulletin point
        # embedding hyperlink -> link link_logo

    def _parse_paragraph(self, block: dict):
        md_text = self._extract_rich_text(block['paragraph']['rich_text'])
        self.output.append(("p", md_text))
    

    def _parse_image(self, block: dict):
        # caption = "".join(word['plain_text'] for word in block['image']['caption'])
        # caption = self._extract_rich_text(block['image']['caption'], only_plain_text=True)
        url = block['image']['file']['url'] if 'file' in block['image'] else block['image']['external']['url']
        # text = f"![{caption}]({url})"

        self.output.append(("img", url))
    

    def _parse_code(self, block: dict):
        code = block['code']
        language = code.get("language", "")
        code_text = "".join(rich_text_part['plain_text'] for rich_text_part in code['rich_text'])
        
        self.output.append(("code", f"""```{language}\n{code_text}\n```"""))


    def _parse_quote(self, block: dict):
        rich_text_extracted = self._extract_rich_text(block['quote']['rich_text'])
        result = "\n>\n".join("> " + line for line in rich_text_extracted.split('\n'))
        self.output.append(("quote", result))


    @staticmethod
    def _extract_rich_text(rich_text: List[dict], only_plain_text=False):
        result: List[str] = []
        for rich_text_part in rich_text:
            if only_plain_text:
                result.append(rich_text_part['plain_text'])
                continue

            if 'href' in rich_text_part and rich_text_part['href']:
                text = f"[{rich_text_part['plain_text']}]({rich_text_part['href']})"
            else:
                text = rich_text_part['plain_text']

            if rich_text_part['annotations']['bold']: text = f"**{text}**"
            if rich_text_part['annotations']['italic']: text = f"*{text}*"
            if rich_text_part['annotations']['strikethrough']: text = f"~~{text}~~"
            if rich_text_part['annotations']['code']: text = f"`{text}`"

            result.append(text)
        
        return "".join(result)


def write_2_markdown_files(page: MomentPage):
    # _name = "".join(char for char in page.page_name if char.isalnum()).strip().repalce(" ", "_")
    file_name: str = f"{page.created_time.strftime(r'%Y%m%d_%H%M')}-{page.page_id[:6]}.md"
    with open(f"content/{file_name}", encoding="utf-8", mode="w") as f:
        f.write(page.to_hugo_md_page_str())


# %%
pages = []
for notion_page in notion_pages:
    # todo change to concurrent parse
    # todo update only recently modified 
    page: MomentPage = MomentPage(raw_page_meta_info=notion_page)
    page.parse()
    pages.append(page)
    # print(page.to_hugo_md_page_str())


# %%
os.mkdir("./content")
for page in pages:
    write_2_markdown_files(page)
