import pygame
import os
import cv2
from tkinter import filedialog
import matplotlib.pyplot
import numpy as np
from sklearn.cluster import KMeans

# basic
pygame.init()
running = True
clock = pygame.time.Clock()
screen = pygame.display.set_mode((900,700))
pygame.display.set_caption("Ứng dụng giảm độ phân giả của ảnh ")

# set color 
black = (0,0,0)
white = (255,255,255)
gray = (218,218,218)

# set font 
font = pygame.font.SysFont('sans',40)
font_small = pygame.font.SysFont('sans',30)
text_img_before = font.render('Image Before',True,white)
text_img_after = font.render('Image After',True,white)
text_select = font.render('Select',True,white)
text_plus = font.render('+',True,white)
text_minus = font.render('-',True,white)
text_run = font.render('Run',True,white)

K = 0 
select_file = ''
run_file = ''
print_test = True
run_kmeans = False


while running:
	mouse_x , mouse_y = pygame.mouse.get_pos()	

	clock.tick(60)
	screen.fill(gray)
	# draw display image 
	pygame.draw.rect(screen,black, (50,50,500,250))
	screen.blit(text_img_before, (200,150))
	pygame.draw.rect(screen,black, (50,380,500,250))
	screen.blit(text_img_after, (200,480))
	# draw button 
		# draw select image in folder computer
	pygame.draw.rect(screen,black, (650,50,200,100))
	screen.blit(text_select, (700,75))
		# draw button +
	pygame.draw.rect(screen,black, (650,180,200,100))
	screen.blit(text_plus, (740,205))
		# draw button -
	pygame.draw.rect(screen,black, (650,310,200,100))
	screen.blit(text_minus, (740,335))
		# draw number image K 
	font_Number = font_small.render('Number color : '+str(K),True,black)
	screen.blit(font_Number, (650,440))
		# draw run
	pygame.draw.rect(screen,black, (650,520,200,100))
	screen.blit(text_run, (715,540))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False 
		if event.type == pygame.MOUSEBUTTONDOWN: 
		# handle button select
			if 650 < mouse_x < 850 and 50 < mouse_y < 150:
				file_path = filedialog.askopenfilename()
				select_file = file_path
				print("select your file")
				
		# handle button +
			if 	650 < mouse_x < 850 and 180 < mouse_y < 280:
				K +=1 
				print("Key +") 
		# handle button - 
			if 	650 < mouse_x < 850 and 310 < mouse_y < 410:
				if K > 0:
					K -=1 
					print("Key -") 
		# handle button run
			if 	650 < mouse_x < 850 and 520 < mouse_y < 620:
				if K > 0 and select_file:
					run_kmeans = True
					print("Key Run") 

	if select_file :
		if file_path.endswith('.png') or file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
			image = pygame.image.load(file_path)
			pygame.image.save(image, "temp_image.png")
			img = matplotlib.pyplot.imread("temp_image.png")
			height, width = img.shape[:2]
			
			if print_test:	
				print(img.shape[0])
				print(img.shape[1])
				print_test = False		
			
			#  khi ảnh cho vào lớn hơn khung
			if height > 250 or width > 500:
				# doChenhLech = 0
				# if height > width:
				# 	doChenhLech = height - width
				# if height < width:
				# 	doChenhLech = width - height
				# print(f"Do chenh lech :{doChenhLech}")	
				# if doChenhLech <= 60:
				# 	flagBreak = True
				# 	while flagBreak:
				# 		print("run program")
				# 		if width >= 500 or height >= 250:
				# 			width -= int(width * (1/3))
				# 			height -= int(height *(1/3))
				# 			print(f"y={height} x={width}")
				# 			if width < 500 and height < 250:
				# 				flagBreak = False
				# else:
				# 	if height > 250 and width > 500:
				# 		flag_Break = True
				# 		while flag_Break:
				# 			width -= int(width * (1/3))
				# 			height -= int(height * (1/3))
				# 			if height < 250 and width < 500:
				# 				flag_Break = False 	
				# 			x_width = (500 - width) // 2 
				# 			y_height = (250 - height) // 2 
				# 	# screen.blit(image, (x_width,y_height))	
				# 	if height <= 250 and width > 500:
				# 		width -= int(width * (1/3))
				# 	if width <= 500 and height > 250:
				# 		height -= int(height * (1/3))
				print(width,height)		
				# imageShow = pygame.transform.scale(image, (width, height)) 
				imageShow = pygame.transform.scale(image, (500, 250)) 

			# vừa với khung 
			else:
				x = (500 - width) // 2
				y = (250 - height) //2
				screen.blit(image, (x, y))
			screen.blit(imageShow, (50,50))

	if run_kmeans == True:		
		imgNew = cv2.imread("temp_image.png")
		width_New = imgNew.shape[0]
		height_New = imgNew.shape[1]

		imgNew = imgNew.reshape(width_New*height_New,3)

		kmeans = KMeans(n_clusters=K).fit(imgNew)
		lables = kmeans.predict(imgNew)
		cluster = kmeans.cluster_centers_

		img_Convert = np.zeros_like(imgNew)
		for i in range(len(img_Convert)):
		 	img_Convert[i] = cluster[lables[i]]
		img_Convert = img_Convert.reshape(width_New,height_New,3)
		
		img_Convert_rgb =  cv2.cvtColor(img_Convert, cv2.COLOR_BGR2RGB)

		# matplotlib.pyplot.imshow(img_Convert_rgb)
		# matplotlib.pyplot.show()
		
		# save image new
		cv2.imwrite('imageConverted.jpg',img_Convert_rgb)
		
		# open image new convert
		imageConverted = cv2.imread("imageConverted.jpg")
		
		width_Converted = imageConverted.shape[0]
		height_Converted = imageConverted.shape[1]
		
		image_Converted_load = pygame.surfarray.make_surface(imageConverted)

		# image_Converted_load = pygame.transform.flip(image_Converted_load, False, True)
		image_Converted_load = pygame.transform.rotate(image_Converted_load, -90)

		if height_Converted > 250 or width_Converted > 500:
			image_Converted_load = pygame.transform.scale(image_Converted_load, (500, 250)) 
		else:
			x = (500 - width_Converted) // 2
			y = (250 - height_Converted) //2
			screen.blit(image_Converted_load, (x, y))
		screen.blit(image_Converted_load, (50,380))
	pygame.display.flip()


pygame.quit()		







