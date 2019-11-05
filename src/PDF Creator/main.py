import os
from fpdf import FPDF
from PIL import Image
import random
import string
import asset


class PDF():
    def __init__(self, output_path, images_list, font='Arial', size=12):
        self.pdf = FPDF(format=(210, 230))
        self.pdf.add_page()
        self.font = font
        self.output_path = output_path
        self.images_list = images_list
        self.pdf.set_draw_color(60, 57, 57)

    def write_line(self, text, x, y, size=14):
        self.pdf.set_xy(x=x, y=y)
        self.pdf.set_font(self.font, size=size)
        self.pdf.cell(w=0, h=5, txt=text)
        self.y_velue = y + 10

    def write_number(self, x, y, size=12):
        self.pdf.set_xy(x=x, y=y)
        self.pdf.set_font(self.font, size=size)
        signs = string.ascii_uppercase + string.digits
        number = 'NO: ' + ''.join(random.sample(signs, 10))
        self.pdf.cell(w=0, h=5, txt=number)
        self.y_velue = y + 5

    def leyout_1(self, image_list):
        id = [i for i in range(len(image_list))]
        random.shuffle(id)
        self.pdf.image(image_list[id[0]], x=10, y=30, w=110, h=85)
        self.pdf.image(image_list[id[1]], x=135, y=30, w=65, h=40)
        self.pdf.image(image_list[id[2]], x=135, y=75, w=65, h=40)
        self.y_velue = 120

    def leyout_2(self, image_list):
        id = [i for i in range(len(image_list))]
        random.shuffle(id)
        self.pdf.image(image_list[id[0]], x=10, y=30, w=90, h=110)
        self.pdf.image(image_list[id[1]], x=110, y=30, w=90, h=110)
        self.y_velue = 145

    def draw_imgs(self):
        def get_img_leyout():
            def get_img_ratio(img_path):
                img = Image.open(img_path)
                w, h = img.size
                return w / h
            ids_above_threshold = []
            ids_belove_threshold = []
            for id, item in enumerate(self.images_list):
                retio = get_img_ratio(item)
                if retio > 1.0:
                    ids_above_threshold.append(item)
                else:
                    ids_belove_threshold.append(item)
            if len(ids_above_threshold) >= 3:
                return self.leyout_1, ids_above_threshold
            return self.leyout_2, ids_belove_threshold
        leyout, ids_list = get_img_leyout()
        leyout(ids_list)

    def draw_horizontal_line(self, x1, x2):
        self.pdf.line(x1, self.y_velue, x2, self.y_velue)
        self.y_velue += 5

    def write_txt(self, text, x, y, size=10):
        self.pdf.set_xy(x=x, y=y)
        self.pdf.set_font("Arial", size=size)
        self.pdf.multi_cell(w=110, h=5, align="J", txt=text)

    def save_file(self):
        self.pdf.output(self.output_path)


cwd = os.getcwd()
input_path = os.path.join(cwd, 'input')
dirs_list = os.listdir(input_path)
pdf_path = os.path.join(cwd, 'PDF')
dirs_list = [item for item in dirs_list if 'valid' in item]
csv_path = os.path.join(cwd, 'realestate.csv')

new_obj = asset.text_generation()
comments = new_obj.open_csv(csv_path)
comments_generator = new_obj.train_me(comments)

# desc, jrooms = new_obj.rest_of_code(summary)
# jrooms = jrooms.split(", ")
for i in range(5):
    for item_ in dirs_list:
        inner_directory = os.path.join(input_path, item_)
        path_to_summary = os.path.join(inner_directory, 'summary.txt')
        lines = [line.rstrip('\n') for line in open(path_to_summary)]
        filenames = new_obj.get_files(path_to_summary)
        rooms = new_obj.count_rooms(filenames)
        jrooms = new_obj.get_jroom(rooms)
        numbers, rooms = new_obj.get_number_rooms(rooms)
        begin = new_obj.do_sth(numbers, rooms)
        description = new_obj.do_sth_2(comments_generator, begin)

        files_list = []
        for line in lines:
            item = line.split(", ")
            files_list.append(os.path.join(inner_directory, item[0]))

        file_name = 'PDF/__' + item_ + str(i) + '.pdf'
        new_pdf = PDF(file_name, files_list)
        new_pdf.write_line(x=10, y=15, size=16, text='Apartment for sale')
        new_pdf.write_number(x=10, y=22)
        new_pdf.draw_imgs()
        new_pdf.draw_horizontal_line(x1=10, x2=200)
        temp_x = new_pdf.y_velue
        new_pdf.write_line(y=new_pdf.y_velue, x=10, text='Description:')


        new_pdf.write_txt(y=new_pdf.y_velue, x=10, text=description)
        new_pdf.write_line(y=temp_x, x=125, text='Details:')

        random.shuffle(jrooms)
        for item in jrooms:
            new_pdf.write_line(y=new_pdf.y_velue, x=125, text=item, size=10)
            new_pdf.y_velue -= 4

        new_pdf.save_file()
