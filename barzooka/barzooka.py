import os
import glob
import requests
from fastai.vision.all import *
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

os.environ['NO_PROXY'] = '127.0.0.1'


class Barzooka(object):
    def __init__(self, model_file='barzooka.pkl'):

        super(Barzooka, self).__init__()
        self.learner = load_learner(model_file)
        self.re_pg = re.compile(r'Index: \d+, Size: (\d+)')

    def predict_from_folder(self, pdf_folder, save_filename,
                            tmp_folder='./tmp/'):
        """Barzooka prediction for folder of publication pdf files"""
        if(tmp_folder == ''):
            raise ValueError("tmp folder argument missing")
        if not os.path.exists(tmp_folder):
            os.mkdir(tmp_folder)

        pdf_table = self.__get_pdf_list(pdf_folder)
        with open(save_filename, "w") as f:
            f.write("approp,bar,pie,hist,bardot,box,dot,violin,flowyes,flowno,paper_id\n")
        for index, row in pdf_table.iterrows():
            paper_id = row['paper_id']
            print(paper_id)
            try:
                barzooka_result = self.predict_from_file(paper_id, tmp_folder)
            except:
                print("Could not screen pdf " + paper_id)

            result_row = pd.DataFrame([barzooka_result])
            result_row.to_csv(save_filename, mode='a', header=False, index=False)

    def predict_from_file(self, pdf_file, tmp_folder='./tmp/', pagewise=False):
        """Barzooka prediction for publication pdf files"""
        # convert pdf to images
        if(tmp_folder == ''):
            raise ValueError("tmp folder argument missing")
        if not os.path.exists(tmp_folder):
            os.mkdir(tmp_folder)

        self.__convert_pdf(pdf_file, tmp_folder)
     	
        images = get_image_files(tmp_folder)

        classes_detected = self.__predict_img_list(images, pagewise)
        doi = pdf_file.split('/')[-1].replace("+", "/").replace(".pdf", "")
        if pagewise == False:
            classes_detected['paper_id'] = doi

        # remove images again
        for j in range(0, len(images)):
            os.remove(images[j])

        return classes_detected

    def predict_from_img(self, img_files):
        """Barzooka prediction for list of image files"""
        classes_detected = self.__predict_img_list(img_files, pagewise = True)
        return classes_detected
        
    def predict_from_img_folder(self, img_folder):
        """Barzooka prediction for folder of image files"""
        images = get_image_files(img_folder)

        # predict on images
        classes_detected = self.__predict_img_list(images, pagewise = True)
        return [images, classes_detected]

    def __get_pdf_list(self, pdf_folder):
        """Searches PDF folder for all PDF filenames and returns them
           as dataframe"""
        pdf_list = []
        for root, dirs, files in os.walk(pdf_folder):
            for filename in files:
                paper_dict = {"paper_id": root + filename}
                pdf_list.append(paper_dict)

        pdf_table = pd.DataFrame(pdf_list)
        return pdf_table

    def __convert_pdf(self, pdf_file, tmp_folder):
        image_filename = pdf_file.split('/')[-1][:-4]
        os.system('pdftocairo -jpeg -scale-to-x 560 -scale-to-y 560 "'
                  + pdf_file + '" "' + tmp_folder + image_filename + '"')

    def __predict_img_list(self, images, pagewise):
        """Predicts graph types for each image & returns pages with bar graphs
        """
        if(type(images) == str):
            images = [images]
        page_predictions = [self.__predict_graph_type(images[idx])
                                     for idx in range(0, len(images))]
        class_names = ['approp', 'bar', 'pie', 'hist', 'bardot', 'box', 'dot', 'violin', 'flowyes','flowno']
        class_counts = [self.__count_class(class_name, page_predictions) for class_name in class_names]
        classes_detected = dict(zip(class_names, class_counts))
        if(pagewise):
            return page_predictions
        return classes_detected

    def __count_class(self, class_name, predictions):
        return [class_name in page for page in predictions].count(True) 

    def __predict_graph_type(self, img):
        """Use fastai model on each image to predict types of pages
        """
        class_names = {
            "0": ["approp"],
            "1": ["bar"],
            "2": ["bardot"],
            "3": ["box"],
            "4": ["dot"],
            "5": ["flowno"],
            "6": ["flowyes"],
            "7": ["hist"],
            "8": ["other"],
            "9": ["pie"],
            "10": ["text"],
            "11": ["violin"]
        }
        pred_class, pred_idx, outputs = self.learner.predict(img)
        if pred_idx.sum().tolist() == 0:
            # if there is no predicted class (=no class over threshold)
            # give out class with highest prediction probability
            highest_pred = str(np.argmax(outputs).tolist())
            pred_class = class_names[highest_pred]
        else:
            pred_class = pred_class.items  # extract class name as text
        return(pred_class)
