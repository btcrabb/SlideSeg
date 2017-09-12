import slideseg
import os

def main():
    """
    Runs SlideSeg with the parameters specified in Parameters.txt
    :return: image chips and masks
    """

    def str2bool(value):
        return value.lower() in ("true", "yes", "1")

    params = slideseg.load_parameters('Parameters.txt')
    print('running __main__ with parameters: {0}'.format(params))

    if str2bool(params["single_slide"]) is True:
        path, filename = os.path.split(params["slide_path"])
        xpath, xml_filename = os.path.split(params["xml_path"])
        params["slide_path"] = path
        params["xml_path"] = xpath

        print('loading {0}'.format(filename))
        slideseg.run(params, filename)

    else:
        for filename in os.listdir(params["slide_path"]):
            slideseg.run(params, filename)

if __name__ == "__main__":
    main()