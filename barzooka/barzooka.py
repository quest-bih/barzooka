import os
import fastai


class Barzooka(object):
    """
    This class offers an interface to the trained
    Barzooka model which handles PDF and image folders/file lists
    as input and gathering the prediction outputs.

    Attrubutes
    ----------
    model_file: str
        trained model file in pkl format

    Methods
    -------
    predict_from_folder(pdf_folder, save_filename, tmp_folder='./tmp/')
        Takes the path of a folder with pdfs and converts each pdf to
        page images using the poppler library and saves them in tmp_folder
        Predictions per pdf are aggregated for all pages. Results per 
        paper are saved in the csv file named save_filename.
    predict_from_file(pdf_file, tmp_folder='./tmp/', pagewise=False)
        Returns the prediction for a single PDF file either 
        aggregated in dict format or on the page level (if pagewise=True).
    predict_from_img_folder(img_folder)
        Calculates predictions for all images in img_folder and returns
        a result list.
    predict_from_img(img_files)
        Takes a list of image file path and calculates predictions
        for all images in the list. Returns a result list.

    """

    def __init__(self, model_file='barzooka.pkl'):
        """
        Parameters
        ----------
        model_file : str
            trained model file in pkl format
        """

        super(Barzooka, self).__init__()
        self.learner = fastai.learner.load_learner(model_file)
        self.class_names = ['approp', 
                            'bar', 
                            'bardot', 
                            'box', 
                            'dot', 
                            'flowno', 
                            'flowyes', 
                            'hist', 
                            'other', 
                            'pie', 
                            'text', 
                            'violin']

    def predict_from_folder(self, pdf_folder, save_filename,
                            tmp_folder='./tmp/'):
        """
        Barzooka prediction for folder of publication pdf files
        Takes the path of a folder with pdfs and converts each pdf to
        page images using the poppler library and saves them in tmp_folder
        Predictions per pdf are aggregated for all pages. Results per 
        paper are saved in the csv file named save_filename. After each
        screened PDF the results are written to the csv file such that
        no results get lost in a long run.

        Requires pre-installed poppler library to use the pdftocairo
        conversion function.

        Parameters
        ----------
        pdf_folder : str
            Folder path for PDF folder.
        save_filename : str
            Filename of csv file in which results get written.
        tmp_folder : str
            Folder used to temporarily extract page images from 
            PDF files. Folder is created if not yet existing.

        """

        if(tmp_folder == ''):
            raise ValueError("tmp folder argument missing")
        if not os.path.exists(tmp_folder):
            os.mkdir(tmp_folder)

        pdf_table = self.__get_pdf_list(pdf_folder)
        colnames = ",".join(self.class_names) + ",paper_id\n"
        with open(save_filename, "w") as f:
            f.write(colnames)
        for index, row in pdf_table.iterrows():
            paper_id = row['paper_id']
            try:
                barzooka_result = self.predict_from_file(paper_id, tmp_folder)
            except:
                print("Could not screen pdf " + paper_id)

            result_row = pd.DataFrame([barzooka_result])
            result_row.to_csv(save_filename, mode='a', header=False, index=False)

    def predict_from_file(self, pdf_file, tmp_folder='./tmp/', pagewise=False):
        """
        Barzooka prediction for publication pdf files
        Returns the prediction for a single PDF file either 
        aggregated in dict format or on the page level (if pagewise=True).

        Parameters
        ----------
        pdf_file : str
            PDF filename that should get screened.
        tmp_folder : str
            Folder used to temporarily extract page images from 
            PDF files. Folder is created if not yet existing.
        pagewise : boolean
            Should the results for each page be given (True)
            or should the results be aggregated for the entire
            PDF (False)?

        Examples
        --------
        >>> b.predict_from_file("barzooka/examples/pdf/doc.pdf")
        {'approp': 0,
         'bar': 0,
         'bardot': 0,
         'box': 3,
         'dot': 4,
         'flowno': 0,
         'flowyes': 0,
         'hist': 0,
         'other': 0,
         'pie': 0,
         'text': 1,
         'violin': 1,
         'paper_id': 'doc'}

        """

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
        """
        Barzooka prediction for list of image files
        Takes a list of image file path and calculates predictions
        for all images in the list. Returns a result list.
        
        Parameters
        ----------
        img_files : list
            List of image file path that should get screened.
        
        Examples
        --------
        >>> b.predict_from_img("barzooka/examples/img/dot1.jpg") 
        [['dot']]
        
        """

        classes_detected = self.__predict_img_list(img_files, pagewise = True)
        return classes_detected
        
    def predict_from_img_folder(self, img_folder):
        """
        Barzooka prediction for folder of image files
        Calculates predictions for all images in img_folder and returns
        a result list.

        Parameters
        ----------
        img_folder : str
            Folder path for image folder.

        Examples
        --------
        >>> b.predict_from_img_folder("barzooka/examples/img")[1]
        [['box'], ['box', 'dot'], ['box', 'dot'], ['dot'], ['dot'], ['text'], ['violin']]

        """

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
        """Converts PDF file to images for all pages and saves them
           in the tmp folder. Requires the poppler library on
           the system.
        """
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
        class_counts = [self.__count_class(class_name, page_predictions) for class_name in self.class_names]
        classes_detected = dict(zip(self.class_names, class_counts))
        if(pagewise):
            return page_predictions
        return classes_detected

    def __count_class(self, class_name, predictions):
        return [class_name in page for page in predictions].count(True) 

    def __predict_graph_type(self, img):
        """Use fastai model on each image to predict types of pages
        """
        class_names_dict = dict(zip(map(str, range(12)), 
                                    [[category] for category in self.class_names]))
        pred_class, pred_idx, outputs = self.learner.predict(img)
        if pred_idx.sum().tolist() == 0:
            # if there is no predicted class (=no class over threshold)
            # give out class with highest prediction probability
            highest_pred = str(np.argmax(outputs).tolist())
            pred_class = class_names_dict[highest_pred]
        else:
            pred_class = pred_class.items  # extract class name as text
        return(pred_class)
