# ***************************************************************
# Maintainers:
#     chuntong pan <panzhang1314@gmail.com>
# Date:
#     2023.12-2024.1
# ***************************************************************
import datetime
import os
import subprocess
import ftplib
import time
from multiprocessing import Pool
import h5py
from PIL import Image
from bs4 import BeautifulSoup
import requests
from michaelPanPrintLib.change_print import print_with_style
import matplotlib.pyplot as plt
from osgeo import gdal, osr, gdal_array
import platform
import matplotlib
import matplotlib.dates as mdates
if platform.system() != "Windows":
	matplotlib.use('Agg')
gdal.UseExceptions()  # 避免osr使用警告
gdal.PushErrorHandler('CPLQuietErrorHandler')
"""
	本程序代码，未经本人许可禁止复制和商用
"""


def select_method(select_str:str):  # 查询这个库里面有哪些方法
	"""
	:param select_str: 任意想要查询的字符串
	:return: None
	"""
	print_with_style(f"该库的关键词有：ovr, matplotlib, tif, modis, file, time等", color='blue')
	all_method_list = ['get_ovr_information方法，查看ovr文件的信息，不用再使用软件查看。',
	                   'draw_many_matplotlib_pic方法，绘制一个主图上有多个子图的图片。',
	                   'generate_ovr方法，使用HDF或PNG或tif数据生成ovr文件。',
	                   'hdf_to_tif方法，HDF文件转换TIF文件。',
	                   'modis_data_mosaic方法，完成modis数据拼接功能。',
	                   'modis_data_projection方法，完成modis数据投影转换功能。',
	                   'modis_data_download方法，完成modis数据下载功能。',
	                   'modis_data_change_res方法，完成modis数据分辨率转换功能。',
	                   'modis_data_clip_china方法，完成modis数据裁剪中国区功能。',
	                   'time_date_num方法，完成时间年月日是一年中第几天的互转功能。',
	                   'time_timestamp_date方法，完成时间戳和日期字符串互相转换功能。',
	                   'trans_file方法，完成文件传输任务。',
	                   ]
	print_with_style(f"输入的查询参数为：{select_str}，查询的结果如下：", color='blue')
	for a_info in all_method_list:
		if select_str in a_info:
			print_with_style(f"   {a_info}", color='cyan')


def get_ovr_information(input_ovr_file:str, show_img=False):  # 查看ovr文件的信息，不用再使用软件查看
	"""
	:param input_ovr_file: 传入的ovr文件路径
	:param show_img: 是否显示图片，默认为False
	:return: None
	"""
	# 打开OVR文件
	ds = gdal.Open(input_ovr_file)
	print_with_style(f"当前打开的ovr文件为：【{os.path.basename(input_ovr_file)}】", color="blue")
	# 获取投影信息
	proj = ds.GetProjection()
	print_with_style(f"该ovr文件的投影信息为：【{proj}】", color="blue")
	# 获取地理变换信息
	geo_transform = ds.GetGeoTransform()
	print_with_style(f"该ovr文件的地理变换信息为：【{geo_transform}】", color="blue")
	# 读取第一个波段的数据到NumPy数组
	band = ds.GetRasterBand(1)
	image = band.ReadAsArray()
	print_with_style(f"该ovr文件的图像尺寸为：【{image.shape}】", color="blue")
	if show_img:
		# 创建pyplot图形
		plt.figure()
		# 显示数组作为灰度图像
		plt.imshow(image, cmap='jet')
		# 不显示坐标轴值
		plt.axis('off')
		plt.show()
	# 关闭数据集
	ds = None


def draw_many_matplotlib_pic(num_plot:list, w_h:list, x_data:list, y_data:list, x_ticks:list, y_ticks:list, x_label:list,
                             y_label:list, x_lim:list,  y_lim:list, sub_title:list, pic_type:list, pic_line_color:list,
                             time_type:list, title:str, save_or_show:str, font_path=None):  # 绘制一个主图上有多个子图的图片
	"""
	:param num_plot: 子图的数量，传入行列数量的列表，例如[12, 10]
	:param w_h: 主图的长和宽，例如[10, 7]
	:param x_data:  每一个子图的x轴数据，先行后列，例如：子图数量是2*2，[[0, 1], [0, 1], [0, 1], [0, 1]]
	:param y_data:  每一个子图的y轴数据，先行后列，例如：子图数量是2*2，[[0, 1], [0, 1], [0, 1], [0, 1]]
	:param x_ticks: 每一个子图的x轴显示，先行后列，例如：子图数量是2*2，[[0.1, 0.9], [0.1, 0.9], [0.1, 0.9], [0.1, 0.9]]
	:param y_ticks: 每一个子图的x轴显示，先行后列，例如：子图数量是2*2，[[0.1, 0.9], [0.1, 0.9], [0.1, 0.9], [0.1, 0.9]]
	:param x_label: 每一个子图的x轴标签，先行后列，例如：子图数量是2*2，['这是x1', '这是x2', '这是x3', '这是x4']
	:param y_label: 每一个子图的y轴标签，先行后列，例如：子图数量是2*2，['这是y1', '这是y2', '这是y3', '这是y4']
	:param x_lim:   每一个子图的x轴范围，先行后列，例如：子图数量是2*2，[[0, 1], [0, 1], [0, 1], [0, 1]]
	:param y_lim:   每一个子图的y轴范围，先行后列，例如：子图数量是2*2，[[0, 1], [0, 1], [0, 1], [0, 1]]
	:param sub_title: 每一个子图的标题，先行后列，例如：子图数量是2*2，['这是标题1', '这是标题2', '这是标题3', '这是标题4']
	:param pic_type: 绘制哪种类型的图有折线、散点、直方图，对应字符串位 line point rectangle，例如：子图数量是2*2，['line', 'line', 'line', 'line']
	:param pic_line_color: 每一个子图颜色，先行后列，例如：子图数量是2*2，['blue', 'blue', 'blue', 'blue']
	:param time_type: 每一个子图是否需要将X轴显示时间,为None是不需要，先行后列，例如：子图数量是2*2，[None, '%m-%d %H', None, None]
	:param title: 主图的标题
	:param save_or_show: 保存或者显示图片，show为展示，传入路径为保存
	:param font_path: 默认为None，当显示中文时需要传入支持中文的字体
	:return: None
	"""
	from matplotlib import font_manager
	if font_path is not None:
		my_font = font_manager.FontProperties(fname=font_path)  # 坐标轴显示中文，simsun.ttc表示字体文件
	fig, ax = plt.subplots(num_plot[0], num_plot[1])
	fig.set_size_inches(w_h[0], w_h[1])
	if font_path is not None:
		fig.suptitle(title, y=0.95, ha='center', fontproperties=my_font)
	else:
		fig.suptitle(title, y=0.95, ha='center')
	count_num = 0
	for i in range(num_plot[0]):
		for j in range(num_plot[1]):
			if pic_type[count_num] == 'line':
				ax[i,j].plot(x_data[count_num], y_data[count_num], color=pic_line_color[count_num])
			elif pic_type[count_num] == 'point':
				ax[i,j].scatter(x_data[count_num], y_data[count_num], c=pic_line_color[count_num])
			elif pic_type[count_num] == 'rectangle':
				ax[i,j].hist(x_data[count_num], y_data[count_num], c=pic_line_color[count_num])
			if time_type[count_num] is not None:
				# 改变时间显示样式
				ax[i,j].xaxis.set_major_formatter(mdates.DateFormatter(time_type[count_num]))
			if x_lim[count_num] is not None:
				ax[i,j].set_xlim(x_lim[count_num])
			if x_ticks[count_num] is not None:
				ax[i,j].set_xticks(x_ticks[count_num])
			if y_ticks[count_num] is not None:
				ax[i,j].set_yticks(y_ticks[count_num])
			if y_lim[count_num] is not None:
				ax[i,j].set_ylim(y_lim[count_num])
			if font_path is not None:
				ax[i,j].set_ylabel(y_label[count_num], fontproperties=my_font)
				ax[i,j].set_xlabel(x_label[count_num], fontproperties=my_font)
				ax[i,j].set_title(sub_title[count_num], fontproperties=my_font)
			else:
				ax[i,j].set_ylabel(y_label[count_num])
				ax[i,j].set_xlabel(x_label[count_num])
				ax[i,j].set_title(sub_title[count_num])
			count_num += 1
	if save_or_show == 'show':
		plt.show()
	else:
		fig.savefig(save_or_show, format='pdf', bbox_inches='tight', dpi=300)
	

def generate_ovr(input_file_path:str, database_name:str, res:float, lon=-180, lat=90, band_name=None):  # HDF或PNG或tif数据生成ovr文件
	"""
	:param input_file_path:  输入的HDF或PNG或tif文件
	:param database_name:  数据集名称
	:param res: 分辨率
	:param lon: 最小经度
	:param lat: 最大维度
	:param band_name: 当数据为多维度数据时使用 如果是2*1440*720的数据 那么band_name就应该是['ab', 'aa']
	:return: None
	"""
	input_file_path_temp = input_file_path.lower()
	output_file_path = f"{os.path.dirname(input_file_path)}/{os.path.basename(input_file_path).split('.')[0]}.{database_name.replace('/', '-')}.tif"
	if input_file_path_temp.endswith('.hdf'):
		# 打开HDF5文件
		hdf5_file = h5py.File(input_file_path, 'r')
		# 获取数据集
		dataset = hdf5_file[database_name][:]
		# 读取为numpy数组
		dataset_list = []
		output_path_list = []
		# --------------判断数据集通道数量-------------
		if dataset.ndim > 2:
			for i in range(dataset.shape[2]):
				if dataset.shape[2] == 2:  # 当第三个维度通道数为2时
					dataset_list.append(dataset[:, :, i])
				elif dataset.shape[0] == 2:
					dataset_list.append(dataset[i, :, :])
				elif dataset.shape[2] > 2:
					dataset_list.append(dataset[:, :, 0])
					break
				elif dataset.shape[0] > 2:
					dataset_list.append(dataset[0, :, :])
					break
		else:
			dataset_list.append(dataset)
		# ------------------------------------------
		for i, dataset in enumerate(dataset_list):
			if len(dataset_list) == 2:  # 当通道数大于1时修改输出文件名
				for_path, file_extension = os.path.splitext(output_file_path)
				if band_name is None:
					print(f'输入为多通道数据，但是配置文件中未给出，请检查')
					output_path = f"{for_path}_{i}{file_extension}"
				else:
					output_path = f"{for_path}-{band_name[i]}{file_extension}"
			else:
				output_path = output_file_path
			# 获取维度
			xsize = dataset.shape[1]
			ysize = dataset.shape[0]
			# 创建GeoTIFF数据集
			gtiff_driver = gdal.GetDriverByName('GTiff')
			gtiff_ds = gtiff_driver.Create(output_file_path, xsize, ysize, 1, gdal.GDT_Float32)
			# 设置投影坐标系
			srs = osr.SpatialReference()
			srs.ImportFromEPSG(4326)  # WGS84经纬度坐标
			gtiff_ds.SetProjection(srs.ExportToWkt())
			# 写入数组数据到GeoTIFF
			gdal_array.BandWriteArray(gtiff_ds.GetRasterBand(1), dataset)
			gdal.AllRegister()
			# 生成ovr金字塔
			gtiff_ds = None
			ds = gdal.Open(output_file_path)
			ds.BuildOverviews(overviewlist=[1, 2, 4, 8, 16, 32, 64, 128, 256])
			ovrds = gdal.Open(output_file_path + '.ovr', gdal.GA_Update)
			ovrds.SetGeoTransform([lon, res, 0, lat, 0, -res])
			proj = osr.SpatialReference()
			proj.SetWellKnownGeogCS('WGS84')
			ovrds.SetProjection(proj.ExportToWkt())
			# 关闭文件
			ovrds = None
			ds = None
			# 删除中间的tif
			os.remove(output_path)
			hdf5_file.close()
		
	elif input_file_path_temp.endswith('.tif'):
		gdal.AllRegister()
		ds = gdal.Open(input_file_path)  # 加了gdal.GA_Update时，读入JPG返回的事none
		ds.BuildOverviews(overviewlist=[1, 2, 4, 8, 16, 32, 64, 128, 256])
		output_path = input_file_path + '.ovr'
		ovrds = gdal.Open(output_path, gdal.GA_Update)
		ovrds.SetGeoTransform([lon, res, 0, lat, 0, -res])
		proj = osr.SpatialReference()
		proj.SetWellKnownGeogCS('WGS84')
		ovrds.SetProjection(proj.ExportToWkt())
	elif input_file_path_temp.endswith('.png'):
		tempimg = Image.open(input_file_path)
		tempimg = tempimg.resize((8192, 4096), Image.ANTIALIAS)
		output_path = f"{os.path.dirname(input_file_path)}/{os.path.basename(input_file_path).split('.')[0]}_change.png"
		tempimg.save(output_path)
		ds = gdal.Open(output_path)
		ds.BuildOverviews(overviewlist=[1, 2, 4, 8, 16, 32])  # , 16, 32, 64, 128, 256
		ds.SetGeoTransform([lon, res, 0, lat, 0, -res])
		proj = osr.SpatialReference()
		proj.SetWellKnownGeogCS('WGS84')
		ds.SetProjection(proj.ExportToWkt())


def hdf_to_tif(input_hdf_file:str, database_name:str, output_tif_file:str):  # HDF文件转换TIF文件
	hdf5_file = h5py.File(input_hdf_file, 'r')
	dset = hdf5_file[database_name]
	hdf5_data = dset[:]
	xsize = dset.shape[1]
	ysize = dset.shape[0]
	# 创建geotiff
	driver = gdal.GetDriverByName("GTiff")
	output_ds = driver.Create(output_tif_file, xsize, ysize, 1, gdal.GDT_Float32)
	# 设置投影
	srs = osr.SpatialReference()
	srs.ImportFromEPSG(4326)
	output_ds.SetProjection(srs.ExportToWkt())
	output_ds.GetRasterBand(1).WriteArray(hdf5_data)
	# 关闭文件
	hdf5_file.close()
	output_ds = None


def modis_data_mosaic(input_path):  # 完成modis数据拼接功能
	"""
	:param input_path: 下载的modis hdf数据路径
	:return: None
	"""
	input_path_list = os.listdir(input_path)
	input_files = []
	count_num = 0
	geotransform = 0
	for a_path in input_path_list:
		a_path = f"{input_path}/{a_path}"
		if a_path.endswith('tif') and 'output_merge' not in a_path:
			if count_num == 0:
				dataset = gdal.Open(a_path)
				geotransform = dataset.GetGeoTransform()
				count_num += 1
			input_files.append(a_path)
	# 新建一个VRT数据集
	output_vrt = f'{input_path}/output.vrt'
	vrt_options = gdal.BuildVRTOptions(resampleAlg='bilinear')
	vrt_ds = gdal.BuildVRT(output_vrt, input_files, options=vrt_options)
	# 为VRT数据集设置geotransform和projection
	projection = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]]'
	vrt_ds.SetProjection(projection)
	vrt_ds.SetGeoTransform(geotransform)
	# 将VRT数据集重新投影并合并到单个GeoTIFF中
	output_geotiff = f'{input_path}/output_merge.tif'
	gdal.Warp(output_geotiff, vrt_ds, dstSRS='EPSG:4326', outputType=gdal.GDT_Float32)
	# 清理内存
	vrt_ds = None
	del vrt_ds
	os.remove(output_vrt)
	print_with_style(f'【{input_path}】路径下的数据拼接成功', color='cyan')


def modis_data_projection(input_path, k1, k2, proj='WGS84'):  # 完成modis数据投影转换功能
	"""
	:param input_path: 下载的hdf文件夹路径
	:param k1: 数组在modis数据集中的位置，例如 0
	:param k2: 数组在modis数据集中的位置，例如 0
	:param proj: 投影方式，可以不填，默认WGS84
	:return: None
	"""
	for a_path in os.listdir(input_path):
		a_path = f"{input_path}/{a_path}"
		if a_path.endswith('hdf'):
			srs = osr.SpatialReference()
			srs.SetWellKnownGeogCS(proj)
			in_ds = gdal.Open(a_path)
			datasets = in_ds.GetSubDatasets()
			output_tif_path = a_path.replace('hdf','tif')
			gdal.Warp(output_tif_path, datasets[k1][k2], dstSRS=srs.ExportToWkt())
	print_with_style(f'【{input_path}】路径下的数据投影转换成功', color='cyan')


def modis_data_change_res(input_file, output_file, res, proj='WGS84'):  # 完成modis数据分辨率转换功能
	"""
	:param input_file: 需要转换的tif文件
	:param output_file: 转换完成后输出的tif文件
	:param res: 需要转换的目标分辨率
	:param proj:  投影方式，可以不填，默认WGS84
	:return: None
	"""
	srs = osr.SpatialReference()
	srs.SetWellKnownGeogCS(proj)
	in_ds = gdal.Open(input_file)
	gdal.Warp(output_file, in_ds, dstSRS=srs.ExportToWkt(), xRes=res, yRes=res)
	print_with_style(f'【{input_file}】文件数据分辨率转换成功', color='cyan')
	
	
def modis_data_clip_china(input_file, output_file):  # 完成modis数据裁剪中国区功能
	cmd_str = "gdalwarp -of GTiff -te 70.0 0.0 140.0 60.0 " + input_file + " " + output_file
	os.system(cmd_str)
	

def modis_data_download(task:str, this_year:int, days_num:str, part_list:list, download_path:str, token1=None):  # 完成modis数据下载功能
	"""
	:param task: 下载任务，例如：MOD11A1
	:param this_year: 下载的年：例如：2023
	:param days_num:  下载的年中第几天，例如253    ps:可以用time_date_num方法转换
	:param part_list:  地区列表，例如["h23v03", "h24v03", "h25v03"]
	:param download_path: 下载的路径，例如：D:/work/temp/LST/156
	:param token1: 可以不添加，当方法中自带token失效时，需要传入新的
	:return: None
	"""
	if token1 is None:
		token1 = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJBUFMgT0F1dGgyIEF1dGhlbnRpY2F0b3IiLCJpYXQiOjE2OTg3MTk5NTUsIm5iZiI6MTY5ODcxOTk1NSwiZXhwIjoxODU2Mzk5OTU1LCJ1aWQiOiJ6b2VsdTIwMjIiLCJlbWFpbF9hZGRyZXNzIjoiMzA0OTQ4MzQ0QHFxLmNvbSIsInRva2VuQ3JlYXRvciI6InpvZWx1MjAyMiJ9.9owE4fUkODF8xQ0DHzbQaQJ2CA7K8IMde896Q4jh0Hg"
	root_url = f"https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/61/{task}"
	output_file_list = []
	download_url_list = []
	alter_url = f"{root_url}{this_year}/{days_num}"
	# 发送GET请求，设置cookies
	response_root = requests.get(alter_url, verify=False)
	if response_root.status_code == 200:
		soup_root = BeautifulSoup(response_root.text, "html.parser")
		link_tags = soup_root.findAll("a")
		# 遍历提取出的元素，获取链接列表
		for a_tag in link_tags:
			a_href = a_tag.get("href")
			if ".hdf" in a_href and a_href != "None":  # 进行数据筛选
				if len(part_list) > 1:  # 指定地区的情况
					a_part = a_href.split(".")[2]  # 地区位置
					if a_part not in part_list:  # 位置不在地区列表的情况
						continue
				else:  # 全部地区的情况
					pass
				file_url = f"{alter_url}/{os.path.basename(a_href)}"
				out_file_path = f"{download_path}/{os.path.basename(a_href)}"
				if file_url in download_url_list:  # 过滤掉重复路径
					continue
				if not os.path.exists(out_file_path):  # 文件不存在时
					download_url_list.append(file_url)
					output_file_list.append(out_file_path)
				else:
					# 获取文件大小（以字节为单位）
					file_size = os.path.getsize(out_file_path)
					file_size_kb = file_size / 1024
					if file_size_kb > 5:
						download_url_list.append(file_url)
						output_file_list.append(out_file_path)
	print_with_style(f"开始下载，总共{len(download_url_list)}个，请耐心等待...", no_color=True)
	if len(download_url_list) > 1:  # 去掉所有数据都存在的情况
		pool = Pool(processes=5)
		for j in range(len(download_url_list)):
			if os.path.exists(output_file_list[j]):  # 如果下载文件存在且文件大小大于20KB时跳过下载
				file_size = int(os.path.getsize(output_file_list[j]) / (1024 * 20))
				if file_size >= 1:
					print_with_style(f"{output_file_list[j]}文件已经存在，跳过下载。", no_color=True)
			pool.apply_async(func=download_func, args=(download_url_list[j], token1, output_file_list[j], j, len(download_url_list)),)
		pool.close()
		pool.join()
	print_with_style(f"{this_year}年第{int(days_num)}天的{task}数据下载完成！", no_color=True)
	

def time_date_num(input_str: str):  # 完成时间年月日是一年中第几天的互转功能
	"""
	:param input_str: 时间字符串，格式为这两种：20230605或2023256，第一种是年月日，第二种是年第几天
	:return: None
	"""
	if len(input_str) == 8:
		input_time = datetime.datetime.strptime(input_str, "%Y%m%d")
		day_of_year = input_time.timetuple().tm_yday
		print_with_style(f"当前日期为{input_str[:4]}年第{day_of_year}天",color='blue')
	elif len(input_str) == 7:
		init_time = datetime.datetime.strptime(f"{input_str[:4]}0101","%Y%m%d")
		finish_time = init_time + datetime.timedelta(days=int(input_str[4:])-1)
		time_str = finish_time.strftime("%Y%m%d")
		print_with_style(f"{input_str[:4]}年第{int(input_str[4:])}天的日期为：{time_str}", color='blue')
	else:
		raise Exception(f"时间字符串位数不对，请检查输入是否正确，当前输入为【{input_str}】")


def time_timestamp_date(input_time):  # 完成时间戳和日期字符串互相转换功能
	"""
	:param input_time: int类型的时间戳或者14位时间字符串(%Y%m%d%H%M%S)
	:return: 时间戳
	"""
	if isinstance(input_time, int) or isinstance(input_time, float):
		# 将时间戳转换成datetime对象
		date = datetime.datetime.fromtimestamp(input_time)
		# 将datetime对象转换成时间字符串
		date_str = date.strftime('%Y%m%d%H%M%S')
		print_with_style(f"时间戳{input_time}对应的时间为：【{date_str}】", color='blue')
	else:
		# 将时间字符串转换为时间戳
		timestamp = time.mktime(time.strptime(input_time, "%Y%m%d%H%M%S"))
		print_with_style(f"日期{input_time}对应的时间戳为：【{timestamp}】", color='blue')
		return timestamp

	
def trans_file(ftp_host:str, ftp_port:int, ftp_username:str, ftp_password:str, local_file:str, server_path:str):  # 完成文件传输任务
	"""
	:param ftp_host:  看名称即可
	:param ftp_port:  看名称即可
	:param ftp_username:  看名称即可
	:param ftp_password:  看名称即可
	:param local_file:  需要上传的本地文件路径
	:param server_path:  ftp服务器路径
	:return: None
	"""
	# 连入Ftp服务器
	ftp = ftplib.FTP()
	ftp.connect(ftp_host, ftp_port)
	ftp.login(ftp_username, ftp_password)
	# 如果目录不存在的话创建目录
	os.makedirs(os.path.dirname(server_path), exist_ok=True)
	# 上传本地文件到FTP服务器
	with open(local_file, "rb") as file:
		ftp.storbinary("STOR " + server_path, file)
	# 关闭FTP连接
	ftp.close()


# -----------------------------------------方法中用到的方法功能区，一般不作单独调用---------------------------------------------
def download_func(file_url, token1, out_file_path, j, i):
	str_html = requests.get(file_url, headers={"Authorization": f"Bearer {token1}"}, verify=False)
	if str_html.status_code != 200:
		print_with_style(f"{file_url}下载失败，状态码为：{str_html.status_code}", no_color=True)
	else:
		command = """wget -c --no-verbose --cut-dirs=3 "{file_url}" --header "Authorization: Bearer {token1}" -O {out_file_path}""".format(
			file_url=file_url, token1=token1, out_file_path=out_file_path)
		subprocess.call(command, shell=True)
		print_with_style(f"{out_file_path}下载完成({j}/{i})", no_color=True)
		print_with_style(f"下载URL为：{file_url}", no_color=True)


