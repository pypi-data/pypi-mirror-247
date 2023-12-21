import json
import mimetypes
import urllib.request

import requests

from magnifai_aut_sdk.aut_auth import AutAuth
from magnifai_aut_sdk.aut_properties import AutProperties, Property


class Magnifai:
    def __init__(self):
        pass

    @classmethod
    def base_request(cls, port, path, execution_id, test_name):
        base_uri = AutProperties.get_property(Property.MAGNIFAI_HOST)
        data = {
            "base_uri": base_uri,
            "port": port,
            "path": path,
            "auth": AutAuth.get_token(),
            "payload": {}
        }

        if execution_id:
            data["payload"]["executionId"] = execution_id
        if test_name:
            data["payload"]["testName"] = test_name
        return data

    @classmethod
    def compare(cls, execution_id, test_name, baseline_image=None, baseline_image_url=None, input_image=None,
                input_image_url=None, min_similarity='70', excluded_areas=None, noise_filter=0):
        """
            Compare the baselineImage with the inputImage and generate a resultImage highlighting the differences if any were found.
            The images must have the same dimensions. For further information, view Swagger.

            :param str execution_id: Execution to which this test belongs.
            :param str test_name: The name of this test.
            :param str baseline_image: Path to baseline image to compare with the input image.
            :param str baseline_image_url: Baseline image to compare with the inputImage from URL.
            :param str input_image: Path to input image to be compared with the baseline image.
            :param str input_image_url: Input image to be compared with the baselineImage from URL.
            :param str min_similarity: Minimum similarity to determine if a test passes or not.
                                         If None, the status will be Undefined.
            :param list excluded_areas: Areas to be ignored when comparing the images.
                                        These areas are defined on the baseline image.
            :param int noise_filter: Areas to be ignored when comparing the images.
                                        These areas are defined on the baseline image.
            :return: The API Response object.
            :rtype: Response
        """

        data = cls.base_request(cls.get_magnifai_api_port(), "/aut-magnifai-api/image-comparison", execution_id,
                                test_name)
        data["files"] = []
        if baseline_image:
            data["files"].append(('baselineImage', (cls.get_input_name(baseline_image), open(
                baseline_image,
                'rb'), mimetypes.guess_type(input_image)[0])))

        if baseline_image_url:
            data['payload']["baselineImageUrl"] = baseline_image_url

        if input_image:
            data["files"].append(('inputImage', (cls.get_input_name(input_image), open(
                input_image,
                'rb'), mimetypes.guess_type(input_image)[0])))

        if input_image_url:
            data['payload']["inputImageUrl"] = input_image_url

        if min_similarity:
            data["payload"]["minSimilarity"] = min_similarity

        if excluded_areas:
            data["payload"]["excludedAreas"] = json.dumps(excluded_areas)
        if noise_filter:
            data["payload"]["noiseFilter"] = noise_filter

        return requests.post(f"{data['base_uri']}{data['path']}",
                             headers={'Authorization': f'Bearer {data["auth"]}'},
                             data=data['payload'],
                             files=data["files"])

    @classmethod
    def flex_compare(cls, execution_id, test_name, baseline_image=None, baseline_image_url=None, input_image=None,
                     input_image_url=None, min_similarity=None, excluded_areas=None):
        """
            Compare the baselineImage with the inputImage and generate a resultImage highlighting the differences if any were found.
            The images may have different dimensions. For further information, view Swagger.

            :param str execution_id: Execution to which this test belongs.
            :param str test_name: The name of this test.
            :param str baseline_image: Path to baseline image to compare with the input image.
            :param str baseline_image_url: Baseline image to compare with the input image from URL.
            :param str input_image: Path to input image to be compared with the baselineImage.
            :param str input_image_url: Input image to be compared with the baselineImage from URL.
            :param str min_similarity: Minimum similarity to determine if a test passes or not.
                                         If None, the status will be Undefined.
            :param list excluded_areas: Areas to be ignored when comparing the images.
                                        These areas are defined on the baseline image.
            :return: The API Response object.
            :rtype: Response
        """
        data = cls.base_request(cls.get_magnifai_api_port(), "/aut-magnifai-api/flex-compare", execution_id,
                                test_name)

        data["files"] = []
        if baseline_image:
            data["files"].append(('baselineImage', (cls.get_input_name(baseline_image), open(
                baseline_image,
                'rb'), mimetypes.guess_type(input_image)[0])))

        if baseline_image_url:
            data['payload']["baselineImageUrl"] = baseline_image_url

        if input_image:
            data["files"].append(('inputImage', (cls.get_input_name(input_image), open(
                input_image,
                'rb'), mimetypes.guess_type(input_image)[0])))

        if input_image_url:
            data['payload']["inputImageUrl"] = input_image_url

        if min_similarity:
            data["payload"]["minSimilarity"] = min_similarity
        if excluded_areas:
            data["payload"]["excludedAreas"] = json.dumps(excluded_areas)

        return requests.post(f"{data['base_uri']}:{data['port']}{data['path']}",
                             headers={'Authorization': f'Bearer {data["auth"]}'},
                             data=data['payload'],
                             files=data["files"])

    @classmethod
    def search(cls, execution_id, test_name, parent_image=None, parent_image_url=None, child_image_url=None,
               child_image=None, min_similarity='70'):
        """
            Search a child image within a parent image. Child image must have the same size as in parent image to be found.
             For further information view Swagger.

            :param str execution_id: Execution to which this test belongs.
            :param str test_name: The name of this test.
            :param str parent_image: Path to the image containing the child images.
            :param str parent_image_url: The image containing the child images from URL.
            :param str child_image: Path to the image to be located within the parent image.
            :param str child_image_url: The image to be located within the parent image from URL.
            :param str min_similarity: Minimum similarity to determine if a test passes or not.
                                         If None, the status will be Undefined.
            :return: The API Response object.
            :rtype: Response
        """
        data = cls.base_request(cls.get_magnifai_api_port(), "/aut-magnifai-api/search", execution_id,
                                test_name)

        data["files"] = []
        if parent_image:
            data["files"].append(('parentImage', (cls.get_input_name(parent_image), open(
                parent_image,
                'rb'), mimetypes.guess_type(parent_image)[0])))

        if parent_image_url:
            data['payload']["parentImageUrl"] = parent_image_url

        if child_image:
            data["files"].append(('childImage', (cls.get_input_name(child_image), open(
                child_image,
                'rb'), mimetypes.guess_type(child_image)[0])))

        if child_image_url:
            data['payload']["childImageUrl"] = child_image_url

        if min_similarity:
            data["payload"]["minSimilarity"] = min_similarity

        return requests.post(f"{data['base_uri']}:{data['port']}{data['path']}",
                             headers={'Authorization': f'Bearer {data["auth"]}'},
                             data=data['payload'],
                             files=data["files"])

    @classmethod
    def flex_search(cls, execution_id, test_name, parent_image=None, parent_image_url=None, child_image_url=None,
                    child_image=None, min_similarity=None):
        """
            Search a child image within a parent image using the flex search algorithm. This allows to find the child image
            even if the size is not the same as in the parent image. For further information, view Swagger.

            :param str execution_id: Execution to which this test belongs.
            :param str test_name: The name of this test.
            :param str parent_image: Path to the image containing the child images.
            :param str parent_image_url: The image containing the child images from URL.
            :param str child_image: Path to the image to be located within the parent image.
            :param str child_image_url: The image to be located within the parent image from URL.
            :param str min_similarity: Minimum similarity to determine if a test passes or not.
                                         If None, the status will be Undefined.
            :return: The API Response object.
            :rtype: Response
        """
        data = cls.base_request(cls.get_magnifai_api_port(), "/aut-magnifai-api/flex-search", execution_id,
                                test_name)
        data["files"] = []
        if parent_image:
            data["files"].append(('parentImage', (cls.get_input_name(parent_image), open(
                parent_image,
                'rb'), mimetypes.guess_type(parent_image)[0])))

        if parent_image_url:
            data['payload']["parentImageUrl"] = parent_image_url

        if child_image:
            data["files"].append(('childImage', (cls.get_input_name(child_image), open(
                child_image,
                'rb'), mimetypes.guess_type(child_image)[0])))

        if child_image_url:
            data['payload']["childImageUrl"] = child_image_url

        if min_similarity:
            data["payload"]["minSimilarity"] = min_similarity

        return requests.post(f"{data['base_uri']}:{data['port']}{data['path']}",
                             headers={'Authorization': f'Bearer {data["auth"]}'},
                             data=data['payload'],
                             files=data["files"])

    @classmethod
    def locate(cls, execution_id, test_name, container_image=None, container_image_url=None, main_image=None,
               main_image_url=None, relative_image=None, relative_image_url=None, min_similarity='70'):
        """
            Locate the relative position of the relative image regarding to mainImage inside the container image.
            For further information, view Swagger.

            :param str execution_id: Execution to which this test belongs.
            :param str test_name: The name of this test.
            :param str container_image: Path to the image containing the searched images.
            :param str container_image_url: The image containing the searched images from URL.
            :param str main_image: Path to the image to be located in the container and used as a reference point for the relative image.
            :param str main_image_url: The image to be located in the container and used as a reference point for the relative image from URL.
            :param str relative_image: Path to the image to be located in the container and give it's relative position to main image.
            :param str relative_image_url: The image to be located in the container and give it's relative position to mainImage from URL.
            :param str min_similarity: Minimum similarity to determine if a test passes or not.
                                         If None, the status will be Undefined.
            :return: The API Response object.
            :rtype: Response
        """

        data = cls.base_request(cls.get_magnifai_api_port(), "/aut-magnifai-api/locate", execution_id,
                                test_name)
        data["files"] = []
        if container_image:
            data["files"].append(('containerImage', (cls.get_input_name(container_image), open(
                container_image,
                'rb'), mimetypes.guess_type(container_image)[0])))

        if container_image_url:
            data['payload']["containerImageUrl"] = container_image_url

        if main_image:
            data["files"].append(('mainImage', (cls.get_input_name(main_image), open(
                main_image,
                'rb'), mimetypes.guess_type(main_image)[0])))

        if main_image_url:
            data['payload']["mainImageUrl"] = main_image_url

        if relative_image:
            data["files"].append(('relativeImage', (cls.get_input_name(relative_image), open(
                relative_image,
                'rb'), mimetypes.guess_type(relative_image)[0])))

        if relative_image_url:
            data['payload']["relativeImageUrl"] = relative_image_url

        if min_similarity:
            data["payload"]["minSimilarity"] = min_similarity

        return requests.post(f"{data['base_uri']}:{data['port']}{data['path']}",
                             headers={'Authorization': f'Bearer {data["auth"]}'},
                             data=data['payload'],
                             files=data["files"])

    @classmethod
    def flex_locate(cls, execution_id, test_name, container_image=None, container_image_url=None, main_image=None,
                    main_image_url=None, relative_image=None, relative_image_url=None, min_similarity=None):
        """
            Locate the relative position of the relative image regarding to main image inside the containerImage using the flex locate algorithm.
            This allows to find the child image even if the size is not the same as in the parent image.
            For further information, view Swagger.

            :param str execution_id: Execution to which this test belongs.
            :param str test_name: The name of this test.
            :param str container_image: Path to the image containing the searched images.
            :param str container_image_url: The image containing the searched images from URL.
            :param str main_image: Path to the image to be located in the container and used as a reference point for the relative image.
            :param str main_image_url: The image to be located in the container and used as a reference point for the relative image from URL.
            :param str relative_image: Path to the image to be located in the container and give it's relative position to main image.
            :param str relative_image_url: The image to be located in the container and give it's relative position to mainImage from URL.
            :param str min_similarity: Minimum similarity to determine if a test passes or not.
                                         If None, the status will be Undefined.
            :return: The API Response object.
            :rtype: Response
        """
        data = cls.base_request(cls.get_magnifai_api_port(), "/aut-magnifai-api/flex-locate", execution_id,
                                test_name)
        data["files"] = []
        if container_image:
            data["files"].append(('containerImage', (cls.get_input_name(container_image), open(
                container_image,
                'rb'), mimetypes.guess_type(container_image)[0])))

        if container_image_url:
            data['payload']["containerImageUrl"] = container_image_url

        if main_image:
            data["files"].append(('mainImage', (cls.get_input_name(main_image), open(
                main_image,
                'rb'), mimetypes.guess_type(main_image)[0])))

        if main_image_url:
            data['payload']["mainImageUrl"] = main_image_url

        if relative_image:
            data["files"].append(('relativeImage', (cls.get_input_name(relative_image), open(
                relative_image,
                'rb'), mimetypes.guess_type(relative_image)[0])))

        if relative_image_url:
            data['payload']["relativeImageUrl"] = relative_image_url

        if min_similarity:
            data["payload"]["minSimilarity"] = min_similarity

        return requests.post(f"{data['base_uri']}:{data['port']}{data['path']}",
                             headers={'Authorization': f'Bearer {data["auth"]}'},
                             data=data['payload'],
                             files=data["files"])

    @staticmethod
    def get_mime_type(file_path):
        mime_type, _ = mimetypes.guess_type(file_path)
        return mime_type

    @classmethod
    def get_content_type(cls, baseline_image_url):
        try:
            address = urllib.request.urlopen(baseline_image_url)
            return address.getheader('Content-Type')
        except Exception as e:
            return None

    @classmethod
    def get_magnifai_api_port(cls):
        return int(
            AutProperties.get_property(Property.MAGNIFAIAPI_PORT) or AutProperties.get_property(Property.MAGNIFAI_PORT))

    @classmethod
    def get_input_name(cls, input):
        return input.split('/')[-1]
