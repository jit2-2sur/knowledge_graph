from langchain_community.document_loaders import BSHTMLLoader


def load_html_files(file):
    try:
        loader = BSHTMLLoader(file)
        data = loader.load()
        print(f'file: {file} loaded successfully...')
        return data
    except Exception as e:
        print('error in loading file ', e)
