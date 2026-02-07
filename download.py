import jmcomic
import os
import time
import yaml

# 常量定义：漫画ID
ALBUM_ID = '444933'

def get_timestamp_folder(custom_config_path="custom_config.yml"):
    """
    读取自定义配置，生成时间戳文件夹路径（不再修改JMComic的配置文件）
    :param custom_config_path: 自定义配置文件路径
    :return: 时间戳文件夹完整路径
    """
    # 1. 读取自定义配置（仅读folder字段，和JMComic配置分离）
    try:
        with open(custom_config_path, "r", encoding="utf-8") as f:
            custom_config = yaml.safe_load(f)
        print("成功读取自定义配置文件")
    except FileNotFoundError:
        print(f"错误：未找到自定义配置文件 {custom_config_path}")
        return None
    except Exception as e:
        print(f"读取自定义配置失败：{e}")
        return None

    # 2. 提取自定义配置参数
    time_format = custom_config["folder"]["time_format"]
    base_path = custom_config["folder"]["base_path"]
    base_path = base_path.replace("C:/User/", "C:/Users/")  # 修正路径

    # 3. 生成时间戳文件夹并创建
    timestamp = time.strftime(time_format, time.localtime())
    timestamp_folder = os.path.join(base_path, timestamp)
    if not os.path.exists(timestamp_folder):
        os.makedirs(timestamp_folder)
        print(f"成功创建时间戳文件夹：{timestamp_folder}")
    else:
        print(f"时间戳文件夹已存在：{timestamp_folder}")

    return timestamp_folder

if __name__ == "__main__":
    # 第一步：读取自定义配置，生成时间戳文件夹
    custom_config_path = "C:/Users/admin/Desktop/new/JMComic-Crawler-Python/custom_config.yml"
    final_base_dir = get_timestamp_folder(custom_config_path)
    
    if not final_base_dir:
        print("生成时间戳文件夹失败，退出程序")
        exit(1)

    # 第二步：加载JMComic的原始配置（无自定义folder字段，不会报错）
    jm_config_path = "C:/Users/admin/Desktop/new/JMComic-Crawler-Python/option.yml"
    option = jmcomic.create_option_by_file(jm_config_path)

    # 第三步：仅修改JMComic配置里的dir_rule.base_dir（核心）
    option.dir_rule.base_dir = final_base_dir
    print("JMComic将使用的下载目录：", option.dir_rule.base_dir)

    # 第四步：下载漫画
    try:
        print(f"\n开始下载漫画（album_id: {ALBUM_ID}）...")
        jmcomic.download_album(ALBUM_ID, option)
        print(f"漫画 {ALBUM_ID} 下载完成！文件保存在：{final_base_dir}")
    except Exception as e:
        print(f"下载失败：{e}")