import jmcomic
import os
import time
import yaml

# 常量定义：漫画ID（修改这里即可切换下载的漫画）
ALBUM_ID = '422933'

def update_base_dir_with_timestamp(config_path="option.yml"):
    """
    读取YAML配置，生成时间戳文件夹，更新dir_rule.base_dir为目标路径
    :param config_path: YAML配置文件路径
    :return: 更新后的配置字典、最终的base_dir路径
    """
    # 1. 读取YAML配置文件
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        print("成功读取配置文件")
    except FileNotFoundError:
        print(f"错误：未找到配置文件 {config_path}")
        return None, None
    except Exception as e:
        print(f"读取配置文件失败：{e}")
        return None, None

    # 2. 提取folder配置中的参数
    time_format = config["folder"]["time_format"]  # 时间格式
    base_path = config["folder"]["base_path"]      # 基础路径

    # 修正Windows路径常见错误：User → Users（可选但建议加）
    base_path = base_path.replace("C:/User/", "C:/Users/")

    # 3. 生成时间戳文件夹名称和完整路径
    timestamp = time.strftime(time_format, time.localtime())  # 生成时间戳
    timestamp_folder = os.path.join(base_path, timestamp)     # 拼接完整路径

    # 4. 自动创建时间戳文件夹（如果不存在）
    if not os.path.exists(timestamp_folder):
        os.makedirs(timestamp_folder)
        print(f"成功创建时间戳文件夹：{timestamp_folder}")
    else:
        print(f"时间戳文件夹已存在：{timestamp_folder}")

    # 5. 替换dir_rule.base_dir为时间戳文件夹路径
    config["dir_rule"]["base_dir"] = timestamp_folder
    print(f"已更新dir_rule.base_dir为：{timestamp_folder}")

    return config, timestamp_folder

if __name__ == "__main__":
    # 第一步：更新配置并生成时间戳文件夹
    config_path = "C:/Users/admin/Desktop/new/JMComic-Crawler-Python/option.yml"
    updated_config, final_base_dir = update_base_dir_with_timestamp(config_path)
    
    # 验证结果：打印更新后的dir_rule.base_dir
    if not updated_config or not final_base_dir:
        print("配置更新失败，退出程序")
        exit(1)
    print("\n最终配置中的dir_rule.base_dir：", updated_config["dir_rule"]["base_dir"])

    # 第二步：让JMComic使用更新后的配置（核心步骤！）
    option = jmcomic.create_option_by_file(config_path)
    # 覆盖option中的dir_rule.base_dir为时间戳路径
    option.dir_rule.base_dir = final_base_dir
    # 验证：打印JMComic实际使用的下载目录
    print("JMComic将使用的下载目录：", option.dir_rule.base_dir)

    # 第三步：下载漫画（传入更新后的option）
    try:
        # 修正1：用f-string格式化字符串，正确显示ID
        print(f"\n开始下载漫画（album_id: {ALBUM_ID}）...")
        # 修正2：直接传常量ALBUM_ID，不要加引号
        jmcomic.download_album(ALBUM_ID, option)
        # 修正1：f-string格式化结果提示
        print(f"漫画 {ALBUM_ID} 下载完成！文件保存在：{final_base_dir}")
    except Exception as e:
        print(f"下载失败：{e}")