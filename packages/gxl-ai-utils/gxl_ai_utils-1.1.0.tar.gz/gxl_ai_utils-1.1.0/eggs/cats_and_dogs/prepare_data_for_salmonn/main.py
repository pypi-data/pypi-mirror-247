import os
import random
import sys

sys.path.append("/home/work_nfs7/xlgeng/code_runner_gxl/gxl_ai_utils/")

from gxl_ai_utils.utils import utils_file, utils_data
from gxl_ai_utils.thread.my_thread import GxlDynamicThreadPool


def do_prepare_data():
    aishell4_raw_scp_dir = '/home/work_nfs7/xlgeng/workspace/wenet_whisper/examples/aishell/s0/dump3/raw/aishell4'
    aishell4_raw_now = '/home/work_nfs6/xlgeng/data/data_scp/aishell4'
    utils_file.makedir_sil(aishell4_raw_now)
    aishell4_prefix = "/home/work_nfs7/xlgeng/workspace/wenet_whisper/examples/aishell/s0/"
    wav_scp = utils_file.load_dict_from_scp(utils_file.join_path(aishell4_raw_scp_dir, "wav.scp"))
    for k, v in wav_scp.items():
        wav_scp[k] = utils_file.join_path(aishell4_prefix, v)
    utils_file.write_dict_to_scp(wav_scp, utils_file.join_path(aishell4_raw_now, "wav.scp"))
    utils_file.copy_file(utils_file.join_path(aishell4_raw_scp_dir, "text"), utils_file.join_path(aishell4_raw_now, "text"))

    ali_near_dir = "/home/work_nfs7/xlgeng/workspace/wenet_whisper/examples/aishell/s0/dump4/raw/Train_Ali_near"
    ali_far_dir = "/home/work_nfs7/xlgeng/workspace/wenet_whisper/examples/aishell/s0/dump2/raw/Train_Ali_far"
    runer = GxlDynamicThreadPool()
    output_root_dir = '/home/41_data/xlgeng/data/shards'
    utils_file.makedir_sil(output_root_dir)
    for dataset_dir in [aishell4_raw_now]:
        dataset_name = os.path.basename(dataset_dir)
        wav_scp_path = os.path.join(dataset_dir, 'wav.scp')
        text_path = os.path.join(dataset_dir, 'text')
        output_dir = os.path.join(output_root_dir, dataset_name)
        runer.add_task(utils_data.do_make_shard_file, [wav_scp_path, text_path, output_dir])
    runer.start()


def do_concat_shards_list():
    now_shard_list__path = "/home/work_nfs7/xlgeng/bsmu_template/wenet_SALMONN/examples/librispeech/salmonn/data/train/data.list.all.shuf"
    now_shard_list__path_2 = "/home/work_nfs7/xlgeng/bsmu_template/wenet_SALMONN/examples/librispeech/salmonn/data/train/data_2.list.all.shuf"
    data_dir = "/home/41_data/xlgeng/data/shards/"
    now_list = utils_file.load_list_file_clean(now_shard_list__path)
    dir_name_list = os.listdir(data_dir)
    for dir_name in dir_name_list:
        list_path = os.path.join(data_dir, dir_name, "shards_list.txt")
        temp_list = utils_file.load_list_file_clean(list_path)
        now_list.extend(temp_list)
    random.shuffle(now_list)
    utils_file.write_list_to_file(now_list, now_shard_list__path_2)


if __name__ == '__main__':
    do_prepare_data()
    do_concat_shards_list()
