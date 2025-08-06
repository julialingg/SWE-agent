import re
import yaml

def convert_txt_to_structured_yaml(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    entries = content.strip().split('\n\n')

    output_data = []
    for idx, entry in enumerate(entries, start=1):
        # 删除 Learn more 及其后面内容（包括 URL 和 JSON 参数）
        entry_cleaned = re.sub(r'Learn more: .*', '', entry).strip()

        # 格式化每一行（YAML 字符串缩进）
        entry_lines = entry_cleaned.splitlines()
        formatted_text = '\n      '.join(line.rstrip() for line in entry_lines)

        item = {
            'env': {
                'deployment': {
                    'type': 'docker',
                    'image': 'a11y/tailwindcss:latest'
                },
                'repo': {
                    'type': 'preexisting',
                    'repo_name': 'app'
                }
            },
            'problem_statement': {
                'type': 'text',
                'text': f"{formatted_text}",
                'id': f"tailwindcss-{idx:02d}"
            }
        }
        output_data.append(item)

    class LiteralStr(str): pass

    def literal_str_representer(dumper, data):
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style="'")

    yaml.add_representer(LiteralStr, literal_str_representer)

    # 确保 text 字段输出为单引号字符串块
    for item in output_data:
        item['problem_statement']['text'] = LiteralStr(item['problem_statement']['text'])

    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump(output_data, f, allow_unicode=True, sort_keys=False, width=1000)


convert_txt_to_structured_yaml(
    input_path="./problem_statement_tailwindcss.txt",
    output_path="single_instance_expert_tailwindcss.yaml"
)
