# Import necessary libraries and modules
import os
from icrawler.builtin import GoogleImageCrawler
from icrawler import ImageDownloader
from PIL import Image
from six import BytesIO

# This part of code is in order to save images with a name. instead of saving an image with the name-0001 it will save it as (for example) henry0001

# Define a new Google Image Crawler class that includes the keyword in the filename
class KeywordGoogleImageCrawler(GoogleImageCrawler):

    def crawl(self,
              keyword,  # keyword for image search
              filters=None,  # optional filters for search
              offset=0,  # offset for search results
              max_num=1000,  # maximum number of search results
              min_size=None,  # optional minimum size of images
              max_size=None,  # optional maximum size of images
              language=None,  # optional language for search
              file_idx_offset=0,  # offset for the index of the files
              overwrite=False):  # optional flag to overwrite existing files

        # If the offset plus the maximum number of results is greater than 1000,
        # limit the maximum number of results to 1000 minus the offset
        if offset + max_num > 1000:
            if offset > 1000:
                # If the offset is greater than 1000, raise an error
                self.logger.error(
                    '"Offset" cannot exceed 1000, otherwise you will get '
                    'duplicated searching results.')
                return
            elif max_num > 1000:
                # If the maximum number of results is greater than 1000, adjust it
                # and issue a warning
                max_num = 1000 - offset
                self.logger.warning(
                    'Due to Google\'s limitation, you can only get the first '
                    '1000 result. "max_num" has been automatically set to %d. '
                    'If you really want to get more than 1000 results, you '
                    'can specify different date ranges.', 1000 - offset)

        # Define arguments for the feeder and downloader
        feeder_kwargs = dict(
            keyword=keyword,
            offset=offset,
            max_num=max_num,
            language=language,
            filters=filters)
        downloader_kwargs = dict(
            keyword=keyword,  # <<< add this line
            max_num=max_num,
            min_size=min_size,
            max_size=max_size,
            file_idx_offset=file_idx_offset,
            overwrite=overwrite)

        # Call the superclass's crawl method with the new arguments
        super(GoogleImageCrawler, self).crawl(
            feeder_kwargs=feeder_kwargs, downloader_kwargs=downloader_kwargs)


# Define a new Image Downloader class that includes the keyword in the filename
class KeywordNameDownloader(ImageDownloader):

    # Define a method for getting the filename
    def get_filename(self, task, default_ext, keyword):
        filename = super(KeywordNameDownloader, self).get_filename(
            task, default_ext)
        return keyword + filename

    # Define a method for deciding whether to keep a file
    def keep_file(self, task, response, min_size=None, max_size=None, **kwargs):
        """Decide whether to keep the image

        Compare image size with ``min_size`` and ``max_size`` to decide.

        Args:
            response (Response): response of requests.
            min_size (tuple or None): minimum size of required images.
            max_size (tuple or None): maximum size of required images.
        Returns:
            bool: whether to keep the image.
        """
        try:
            img = Image.open(BytesIO(response.content))
        except (IOError, OSError):
            return False
        task['img_size'] = img.size
        if min_size and not self._size_gt(img.size, min_size):
            return False
        if max_size and not self._size_lt(img.size, max_size):
            return False
        return True

    def download(self,
                 task,
                 default_ext,
                 timeout=5,
                 max_retry=3,
                 overwrite=False,
                 **kwargs):
        """Download the image and save it to the corresponding path.

        Args:
            task (dict): The task dict got from ``task_queue``.
            timeout (int): Timeout of making requests for downloading images.
            max_retry (int): the max retry times if the request fails.
            **kwargs: reserved arguments for overriding.
        """
        file_url = task['file_url']
        task['success'] = False
        task['filename'] = None
        retry = max_retry
        keyword = kwargs['keyword']

        if not overwrite:
            with self.lock:
                self.fetched_num += 1
                filename = self.get_filename(task, default_ext, keyword)
                if self.storage.exists(filename):
                    self.logger.info('skip downloading file %s', filename)
                    return
                self.fetched_num -= 1

        while retry > 0 and not self.signal.get('reach_max_num'):
            try:
                response = self.session.get(file_url, timeout=timeout)
            except Exception as e:
                self.logger.error('Exception caught when downloading file %s, '
                                  'error: %s, remaining retry times: %d',
                                  file_url, e, retry - 1)
            else:
                if self.reach_max_num():
                    self.signal.set(reach_max_num=True)
                    break
                elif response.status_code != 200:
                    self.logger.error('Response status code %d, file %s',
                                      response.status_code, file_url)
                    break
                elif not self.keep_file(task, response, **kwargs):
                    break
                with self.lock:
                    self.fetched_num += 1
                    filename = self.get_filename(task, default_ext, keyword)
                self.logger.info('image #%s\t%s', self.fetched_num, file_url)
                self.storage.write(filename, response.content)
                task['success'] = True
                task['filename'] = filename
                break
            finally:
                retry -= 1


# This function finds and downloads face images of a celebrity from Google
# and saves them to a specified directory.
# It returns the name of the last downloaded image.
# The function takes three parameters:
# - name: the name of the celebrity for whom to find face images
# - number: the number of images to download
# - path: the directory where to save the downloaded images
def findFace(name, number, path):
    # Create an instance of the KeywordGoogleImageCrawler class to connect to Google
    # Set the downloader_cls parameter to KeywordNameDownloader to download images that match the search term
    # Set the storage parameter to specify the directory where the downloaded images will be saved
    google_crawler = KeywordGoogleImageCrawler(downloader_cls=KeywordNameDownloader, storage={'root_dir': rf'{path}'})

    # Start the crawling process to find and download images of the celebrity's face
    # The keyword parameter specifies the search term to be used, which is the celebrity's name followed by the word "face"
    # The max_num parameter specifies the maximum number of images to download
    google_crawler.crawl(keyword=name + " face", max_num=number)
    list = os.listdir(path)
    # Get the name of the last downloaded file
    new_name = list[-1]
    return new_name


if __name__=="__main__":
    # Search a name in google and download the 2 first options that were given
    # google_crawler = KeywordGoogleImageCrawler(downloader_cls=KeywordNameDownloader, storage={'root_dir': r'C:\Users\User\Pictures\RandIMG'})
    # while True:
    #     key=input("enter name")
    #     google_crawler.crawl(keyword=key+" face", max_num=2)
    print(findFace("Adele",1,r'C:\Users\User\Pictures\RandIMG'))
