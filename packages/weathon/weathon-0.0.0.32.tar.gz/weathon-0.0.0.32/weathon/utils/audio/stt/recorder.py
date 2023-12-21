import speech_recognition as sr
import time, os
import numpy as np
import logging
from weathon.utils.audio.stt.whisper import Whisper
from weathon.utils.logger import get_logger


class Recorder:
    """
    录音控制类:录音类可以用于监听麦克风输入的音频并调用语音识别类进行识别。通过设置采样率、适应环境时长、录音最长时长等参数，实现自动判断说话开始和结束的功能。
    """

    def __init__(self, save_path="record_audios", sample_rate: int = 16000, adjust_time: int = 2,
                 phrase_limit_time: int = 5,is_save_audio: bool = False, is_transcribe=False):
        """
        :param sample_rate: 采样率
        :param adjust_time: 适应环境时长/s
        :param phrase_limit_time: 录音最长时长/s
        :param is_save_audio: 是否保存音频
        :param is_transcribe: 是否进行文本转语音
        """
        self.sample_rate = sample_rate
        self.duration = adjust_time
        self.phrase_time = phrase_limit_time
        # 用于设置运行状态
        self.running = False
        self.rec = sr.Recognizer()
        self.rec.energy_threshold = 5000
        self.rec.dynamic_energy_ratio = 6
        self.rec.dynamic_energy_adjustment_damping = 0.85
        self.rec.non_speaking_duration = 0.5
        self.rec.pause_threshold = 0.8
        self.rec.phrase_threshold = 0.5        # 麦克风对象

        self.mic = sr.Microphone(sample_rate=self.sample_rate)
        self.save_audio = is_save_audio
        self.transcribe = is_transcribe
        self.save_path = save_path
        self.logger = get_logger(log_level=logging.DEBUG)
        if is_transcribe:
            # 语音识别模型对象
            self.model = Whisper()

    def run(self) -> None:
        self.listen()

    def stop(self) -> None:
        self.running = False

    def listen(self) -> None:
        """
        语音监听函数
        """
        try:
            with self.mic as source:
                # 设备监控
                audio_index = self.mic.audio.get_default_input_device_info()['index']
                work_audio = self.mic.list_working_microphones()
                if len(work_audio) == 0 or audio_index not in work_audio:
                    self.logger.warning("未检测到有效音频输入设备！！！", type='warning')
                    return

                # 录音起始
                self.rec.adjust_for_ambient_noise(source, duration=self.duration)
                self.logger.info("录音开始")
                self.running = True
                while self.running:
                    # 录音中
                    self.logger.info("正在录音...")
                    # self.running为否无法立即退出该函数，如果想立即退出则需要重写该函数
                    audio = self.rec.listen(source, phrase_time_limit=self.phrase_time)
                    # 将音频二进制数据转换为numpy类型
                    audio_np = self.bytes2np(audio.frame_data)
                    if self.save_audio:
                        self.save_wav(audio)
                    # 判断音频rms值是否超过经验阈值，如果没超过表明为环境噪声
                    if np.sqrt(np.mean(audio_np ** 2)) < 0.02:
                        continue
                    if self.transcribe:
                        self.logger.info("音频正在识别")
                        # 识别语音
                        text = self.model.get_instance().transcribe(audio_np)
                        self.logger.info("音频正在识别")

        except Exception as e:
            self.logger.error(e)
        finally:
            self.logger.info("录音停止")
            self.running = False

    def bytes2np(self, inp: bytes, sample_width: int = 2) -> np.ndarray:
        """
        将音频二进制数据转换为numpy类型
        :param inp: 输入音频二进制流
        :param sampleWidth: 音频采样宽度
        :return: 音频numpy数组
        """

        # 使用np.frombuffer函数将字节序列转换为numpy数组
        tmp = np.frombuffer(inp, dtype=np.int16 if sample_width == 2 else np.int8)
        # 确保tmp为numpy数组
        tmp = np.asarray(tmp)

        # 获取tmp数组元素的数据类型信息
        i = np.iinfo(tmp.dtype)
        # 计算tmp元素的绝对最大值
        absmax = 2 ** (i.bits - 1)
        # 计算tmp元素的偏移量
        offset = i.min + absmax

        # 将tmp数组元素转换为浮点型，并进行归一化
        array = np.frombuffer((tmp.astype(np.float32) - offset) / absmax, dtype=np.float32)

        # 返回转换后的numpy数组
        return array

    def save_wav(self, audio: sr.AudioData) -> None:
        """
        保存语音结果
        :param audio: AudioData音频对象
        """
        now_time = time.strftime("%H_%M_%S", time.localtime())
        os.makedirs(self.save_path, exist_ok=True)
        with open("{}/{}.wav".format(self.save_path, now_time), 'wb') as f:
            f.write(audio.get_wav_data())


if __name__ == '__main__':
    recorder = Recorder(is_transcribe=True)
    recorder.listen()
