import io
import os
import requests
import lxml.etree as ET
import re

from .mets import get_title_from_mets, replace_img_urls_in_mets
from .iiif import get_title_from_iiif

base_url = "https://transkribus.eu/TrpServer/rest"
nsmap = {"page": "http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15"}
crowd_base_url = (
    "https://transkribus.eu/r/read/sandbox/application/?colId={}&docId={}&pageId={}"
)


class ACDHTranskribusUtils:
    def login(self, user, pw):
        """log in function
        :param user: Your TRANSKRIBUS user name, e.g. my.mail@whatever.com
        :param pw: Your TRANSKRIBUS password
        :param base_url: The base URL of the TRANSKRIBUS API
        :return: The Session ID in case of a successful log in attempt
        """
        request_url = f"{self.base_url}/auth/login"
        res = requests.post(request_url, data={"user": user, "pw": pw})
        if res.status_code == 200:
            tree = ET.fromstring(res.content)
            sessionid = tree.xpath("/trpUserLogin/sessionId/text()")
            cookies = dict(JSESSIONID=sessionid[0])
            return cookies
        elif res.status_code == 403:
            raise Exception(
                f"Unable to authenticate to the Trancribus-server ({request_url}) with the provided credentials."
                "\nCheck if you provided the correct username & password."
                "\nPasswords/usernames containing special characters, spaces etc. may cause this behaviour. "
                "So you might need to change your password."
            )
        else:
            raise Exception(
                f"Login at Transcribus-server ({request_url}) failed with unexspected http-status code '{res.status_code}'."  # noqa
            )

    def ft_search(self, **kwargs):
        """ Helper function to interact with TRANSKRIBUS fulltext search endpoint
            :param kwargs: kwargs will be forwarded to TRANSKRIBUS API endpoint e.g. 'query' holds the\
            search string
            :return: The default TRANSKRIBUS response as JSON
        """
        url = f"{self.base_url}/search/fulltext"
        if kwargs:
            querystring = kwargs
        else:
            return False
        querystring["type"] = "LinesLc"
        print(querystring)
        response = requests.request(
            "GET", url, cookies=self.login_cookie, params=querystring
        )
        if response.ok:
            return response.json()
        else:
            return response.ok

    def list_collections(self):
        """Helper function to list all collections
        :return: A dict with listing the collections
        """
        url = f"{self.base_url}/collections/list"
        response = requests.get(url, cookies=self.login_cookie)
        return response.json()

    def filter_collections_by_name(self, filter_string):
        """lists all collections which names contains 'filter_string' collections
        :param filter_string: a string the collection name should contain
        :return: A list with all filtered the collections
        """
        cols = self.list_collections()
        filtered_cols = [x for x in cols if filter_string in x["colName"]]
        return filtered_cols

    def list_docs(self, col_id):
        """Helper function to list all documents in a given collection
        :param col_id: Collection ID
        :return: A dict with listing the collections
        """
        url = f"{self.base_url}/collections/{col_id}/list"
        print(url)
        response = requests.get(url, cookies=self.login_cookie)
        return response.json()

    def get_doc_md(self, doc_id, col_id):
        """Helper function to interact with TRANSKRIBUS document metadata endpoint
        :param col_id: The ID of a TRANSKRIBUS Collection
        :param doc_id: The ID of TRANSKRIBUS Document
        :param page_id: The page number of the Document
        :return: A dict with basic metadata of a transkribus Document
        """
        url = f"{self.base_url}/collections/{col_id}/{doc_id}/metadata"
        response = requests.get(url, cookies=self.login_cookie)
        return response.json()

    def get_doc_overview_md(self, doc_id, col_id):
        """Helper function to interact with TRANSKRIBUS document endpoint
        :param col_id: The ID of a TRANSKRIBUS Collection
        :param doc_id: The ID of TRANSKRIBUS Document
        :return: A dict with basic metadata of a transkribus Document
        """
        url = f"{self.base_url}/collections/{col_id}/{doc_id}/fulldoc"
        response = requests.get(url, cookies=self.login_cookie)
        if response.ok:
            result = {}
            result["trp_return"] = response.json()
            page_list = result["trp_return"]["pageList"]["pages"]
            result["pages"] = [
                {
                    "page_id": x["pageId"],
                    "doc_id": x["docId"],
                    "page_nr": x["pageNr"],
                    "thumb": x["thumbUrl"],
                }
                for x in page_list
            ]
            return result
        else:
            return response.ok

    def get_fulldoc_md(self, doc_id, col_id, page_id="1"):
        """Helper function to interact with TRANSKRIBUS document endpoint
        :param col_id: The ID of a TRANSKRIBUS Collection
        :param doc_id: The ID of TRANSKRIBUS Document
        :param page_id: The page number of the Document
        :return: A dict with basic metadata of a transkribus Document
        """
        url = f"{self.base_url}/collections/{col_id}/{doc_id}/{page_id}"
        response = requests.get(url, cookies=self.login_cookie)
        if response.ok:
            doc_xml = ET.fromstring(response.text.encode("utf8"))
            result = {
                "doc_id": doc_id,
                "base_url": self.base_url,
                "col_id": col_id,
                "page_id": page_id,
                "session_id": self.login_cookie["JSESSIONID"],
            }
            result["doc_url"] = url
            result["doc_xml"] = doc_xml
            result["transcript_url"] = doc_xml.xpath(
                "//tsList/transcripts[1]/url/text()"
            )[0]
            result["thumb_url"] = doc_xml.xpath("./thumbUrl/text()")[0]
            result["img_url"] = doc_xml.xpath("./url/text()")[0]
            result["img_url"] = doc_xml.xpath("./url/text()")[0]
            result["extra_info"] = self.get_doc_md(
                doc_id, col_id=col_id
            )
            return result
        else:
            return response.ok

    def get_transcript(self, fulldoc_md):
        """Helper function to fetch the (latest) fulltext of a TRANSKRIBUS page
        :param fulldoc_md: A dict returned by login.get_fulldoc_md
        :return: The fulldoc_md dict with additional keys 'page_xml' and 'transcript'
        """
        nsmap = {
            "page": "http://schema.primaresearch.org/PAGE/gts/pagecontent/2013-07-15"
        }
        md = fulldoc_md
        url = md["transcript_url"]
        response = requests.get(url, cookies=self.login_cookie)
        if response.ok:
            page = ET.fromstring(response.text.encode("utf8"))
            md["page_xml"] = page
            md["transcript"] = page.xpath(
                ".//page:TextLine//page:Unicode/text()", namespaces=nsmap
            )
            return md
        else:
            return response.ok

    def list_documents(self, col_id):
        """Helper function to interact with TRANSKRIBUS collection endpoint to list all documents
        :param col_id: The ID of a TRANSKRIBUS Collection
        :return: A dict with the default TRANSKRIBUS API return
        """
        url = f"{self.base_url}/collections/{col_id}/list"
        response = requests.get(url, cookies=self.login_cookie)
        if response.ok:
            return response.json()
        else:
            return response.ok

    def get_mets(self, doc_id, col_id):
        """Get METS file from Document
        :param col_id: The ID of a TRANSKRIBUS Collection
        :param doc_id: The ID of TRANSKRIBUS Document
        :return: A dict with an lxml object of the mets file and the doc_id
        """
        url = f"{self.base_url}/collections/{col_id}/{doc_id}/mets"
        response = requests.get(url, cookies=self.login_cookie)
        if response.ok:
            result = {
                "doc_xml": ET.fromstring(response.text.encode("utf8")),
                "doc_id": doc_id,
            }
        else:
            result = {"doc_xml": None, "doc_id": doc_id}
        return result

    def save_mets_to_file(self, doc_id, col_id, file_path="."):
        """Saves the METS file of a Document
        :param col_id: The ID of a TRANSKRIBUS Collection
        :param doc_id: The ID of TRANSKRIBUS Document
        :return: The full filename
        """
        mets_dict = self.get_mets(doc_id, col_id)
        file_name = os.path.join(file_path, f"{mets_dict['doc_id']}_mets.xml")
        if os.path.isdir(file_path):
            with open(file_name, "wb") as f:
                f.write(ET.tostring(mets_dict["doc_xml"]))
            return file_name
        else:
            print(f"{file_path} does not exist")
            return None

    def get_image_names(self, doc_id, col_id):
        """Get images names for Document
        :param col_id: The ID of a TRANSKRIBUS Collection
        :param doc_id: The ID of TRANSKRIBUS Document
        :return: a list of images names
        """
        url = f"{self.base_url}/collections/{col_id}/{doc_id}/imageNames"
        response = requests.get(url, cookies=self.login_cookie)
        if response.ok:
            result = response.text.split("\n")
        else:
            result = []
        return result

    def save_image_names_to_file(self, doc_id, col_id, file_path="."):
        """Saves the METS file of a Document
        :param col_id: The ID of a TRANSKRIBUS Collection
        :param doc_id: The ID of TRANSKRIBUS Document
        :return: The full filename
        """
        file_list = self.get_image_names(doc_id, col_id)
        file_name = os.path.join(file_path, f"{doc_id}_image_name.xml")
        root = ET.Element("list")
        counter = 1
        for x in file_list:
            item = ET.Element("item")
            item.attrib["n"] = f"{counter}"
            item.text = x
            root.append(item)
            counter += 1
        if os.path.isdir(file_path):
            with open(file_name, "wb") as f:
                f.write(ET.tostring(root))
            return file_name
        else:
            print(f"{file_path} does not exist")
            return None

    def collection_to_mets(self, col_id, file_path=".", filter_by_doc_ids=[]):
        """Saves METS files of all Documents from a TRANSKRIBUS Collection
        :param col_id: The ID of a TRANSKRIBUS Collection
        :param doc_id: The ID of TRANSKRIBUS Document
        :param filter_by_doc_ids: Only process documents with the passed in IDs
        :return: The full filename
        """
        mpr_docs = self.list_docs(col_id)
        col_dir = os.path.join(file_path, f"{col_id}")
        try:
            os.makedirs(col_dir)
        except FileExistsError:
            pass
        doc_ids = [x["docId"] for x in mpr_docs]
        if filter_by_doc_ids:
            filter_as_int = [int(x) for x in filter_by_doc_ids]
            doc_ids = [x for x in doc_ids if int(x) in filter_as_int]
        print(f"{len(doc_ids)} to download")
        counter = 1
        for doc_id in doc_ids:
            try:
                save_mets = self.save_mets_to_file(doc_id, col_id, file_path=col_dir)
            except Exception as e:
                print(f"failed to save mets for DOC-ID: {doc_id} in COLLECTION: {col_id} due to ERROR: {e}")
                counter += 1
                continue
            file_list = self.save_image_names_to_file(doc_id, col_id, file_path=col_dir)
            print(f"saving: {save_mets}")
            print(f"saving: {file_list}")
            print(f"{counter}/{len(doc_ids)}")
            counter += 1

        return doc_ids

    def search_for_document(self, title, col_id):
        """Searches for a document with given title in a collection
        :param col_id: The ID of a TRANSKRIBUS Collection
        :param title: Title of the document
        """
        res = requests.get(
            f"{self.base_url}/collections/findDocuments",
            cookies=self.login_cookie,
            params={"collId": col_id, "title": title},
        )
        return res.json()

    def search_for_collection(self, title):
        """Searches for a collection by title
        :param title: Title of the TRANSKRIBUS Collection
        """
        res = requests.get(
            f"{self.base_url}/collections/listByName",
            cookies=self.login_cookie,
            params={"name": title},
            headers={"Accept": "application/json"},
        )
        return res.json()

    def create_collection(self, title):
        """Creates a new collection and returns the collectionId
        :param title: Title of the TRANSKRIBUS Collection
        """
        res = requests.post(
            f"{self.base_url}/collections/createCollection",
            cookies=self.login_cookie,
            params={"collName": title},
        )
        if res.status_code == 200:
            return res.content.decode("utf8")
        else:
            print("error: ", res.status_code, res.content)
            return False

    def get_or_create_collection(self, title):
        """Get or create TRANSKRIBUS collection ID
        :param title: Title of the TRANSKRIBUS Collection
        """
        col = self.search_for_collection(title=title)
        if len(col) == 0:
            col = self.create_collection(title=title)
            return col
        else:
            print(col)
            return col[0]["colId"]

    def upload_mets_file_from_url(self, mets_url, col_id, better_images=False):
        """Takes an URL to a METS file and posts that URL to Transkribus
        :param mets_url: URL of the METS file
        :param col_id: Transkribus CollectionID
        """
        doc_title = get_title_from_mets(mets_url)
        doc_exists = self.search_for_document(title=doc_title, col_id=col_id)
        if len(doc_exists) == 0:
            if better_images:
                new_mets_str = replace_img_urls_in_mets(mets_url)
                new_mets_file = io.BytesIO(new_mets_str.encode("utf-8"))
                files = [("mets", ("mets.xml", new_mets_file, "text/xml"))]
                url = f"{self.base_url}/collections/{col_id}/createDocFromMets?colId={col_id}"
                res = requests.post(url, cookies=self.login_cookie, files=files)
                if res.status_code == 200:
                    return True
                else:
                    print("Error: ", res.status_code, res.content)
                    return False
            else:
                res = requests.post(
                    f"{self.base_url}/collections/{col_id}/createDocFromMetsUrl",
                    cookies=self.login_cookie,
                    params={"fileName": mets_url},
                )
                if res.status_code == 200:
                    return True
                else:
                    print("Error: ", res.status_code, res.content)
                    return False
        else:
            print(
                f"a document with title: {doc_title} already exists in collection {col_id}"
            )
            return False

    def upload_mets_files_from_goobi(
        self, file_titles, check_name=True, col_regex=None, col_id=None
    ):
        """Uploads all file_ids from Goobi via METS in Transkribus
        :param file_titles: Array with file titles to upload
        :param col_id: The ID of a TRANSKRIBUS Collection
        :param check_name (boolean): If set to True checks first if file exist and omits upload if file already exists
        :param col_regex: regex to be used to create collection from file name
        """
        if col_regex is None and col_id is None:
            raise AttributeError("You need to specify either col_regex or col_id")
        pattern = False
        if col_id is None:
            pattern = re.compile(col_regex)
        for f in file_titles:
            if pattern:
                col_name = pattern.match(f)
                col_id = self.get_or_create_collection(col_name.group())
            if check_name:
                s1 = self.search_for_document(f, col_id)
                if len(s1) == 0:
                    self.upload_mets_file_from_url(
                        self.goobi_base_url.format(f), col_id=col_id
                    )

    def upload_iiif_from_url(self, iiif_url, col_id):
        """Takes an URL to a IIIF Manifest and posts that URL to Transkribus
        :param iiif_url: URL of the IIIF Manifest
        :param col_id: Transkribus CollectionID
        """
        # ToDo: check if document with same title already exists
        doc_title = get_title_from_iiif(iiif_url)
        doc_exists = self.search_for_document(title=doc_title, col_id=col_id)
        if len(doc_exists) == 0:
            res = requests.post(
                f"{self.base_url}/collections/{col_id}/createDocFromIiifUrl",
                cookies=self.login_cookie,
                params={"fileName": iiif_url},
            )
            if res.status_code == 200:
                return True
            else:
                print("Error: ", res.status_code, res.content)
                return False
        else:
            print(
                f"a document with title: {doc_title} already exists in collection {col_id}"
            )
            return False

    def get_user_id(self, user_name: str) -> int:
        """returns the ID of the passed in user name
        :param user_name: the user name

        :return: the user's ID
        """
        r = requests.get(
            f"{self.base_url}/user/list",
            cookies=self.login_cookie,
            params={"user": user_name},
        )
        response = r.json()
        user_id = response["trpUser"][0]["userId"]
        return user_id

    def add_user_to_collection(
        self, user_name: str, col_id: int, role: str = "Owner", send_mail: bool = True
    ) -> str:
        """adds user to given collection"""
        user_id = self.get_user_id(user_name)
        result_msg = (
            f"looks like something went wront adding {user_name} to collection {col_id}"
        )
        params = {"userid": user_id, "role": role}
        if not send_mail:
            params = {"userid": user_id, "role": role, "sendMail": False}
        res = requests.post(
            f"{self.base_url}/collections/{col_id}/addOrModifyUserInCollection",
            cookies=self.login_cookie,
            params=params,
        )
        if res.status_code == 200:
            result_msg = f"added user {user_name} to collection {col_id}"
        return result_msg

    def create_status_report(
        self, filter_string: str, transcription_threshold: int = 10
    ) -> list:
        """generates a report about the documents in the filterd collections
        :param filter_string: a string the collection name should contain
        :param transcription_threshold: minimum number of transcribed lines
        to qualify a document as transcribed

        :return: a list dicts
        """
        cols = self.filter_collections_by_name(filter_string)
        print(f"found {len(cols)} matching {filter_string}")
        docs = []
        for x in cols:
            col_id = x["colId"]
            doc_list = self.list_docs(col_id)
            print(f"processing {len(doc_list)} documents from collection {col_id}")
            for y in doc_list:
                transcribed = False
                doc_id = y["docId"]
                doc_overview = self.get_doc_overview_md(doc_id, col_id)
                doc_md = doc_overview["trp_return"]["md"]
                transcribed_lines = doc_md["nrOfTranscribedLines"]
                if transcribed_lines > transcription_threshold:
                    transcribed = True
                doc_stats = {
                    "doc_id": doc_id,
                    "col_id": col_id,
                    "doc_title": doc_md["title"],
                    "doc_transcribed": transcribed,
                    "pages": doc_md["nrOfPages"],
                    "doc_thumb": doc_md["thumbUrl"],
                    "doc_md": doc_md,
                }
                docs.append(doc_stats)
        return docs

    def run_htr(
        self,
        col_id: int | str,
        doc_id: int | str,
        start_page: int = 1,
        end_page: None | int = None,
        model_id: int = 51170,
    ):
        """starts htr with the given params and returns the job ID"""
        job_id = None

        if end_page:
            pages = f"{start_page}-{end_page}"
        else:
            pages = f"{start_page}"
        params = {"id": doc_id, "pages": pages}
        res = requests.post(
            f"{self.base_url}/recognition/{col_id}/{model_id}/trhtr",
            cookies=self.login_cookie,
            params=params,
        )
        if res.status_code == 200:
            job_id = res.text
            print(f"started HTR for DOC-ID: {doc_id} with JOB-ID {job_id}")
            return job_id
        else:
            print("something went wrong")

    def __init__(
        self,
        user=None,
        password=None,
        transkribus_base_url=base_url,
        goobi_base_url=None,
    ) -> None:
        if user is None:
            user = os.environ.get("TRANSKRIBUS_USER", None)
            self.user = user
            if user is None:
                raise AttributeError(
                    "Transkribus username needs to be set in environments or in init"
                )
        else:
            self.user = user
        if password is None:
            password = os.environ.get("TRANSKRIBUS_PASSWORD", None)
            if password is None:
                raise AttributeError(
                    "Transkribus password needs to be set in environments or in init"
                )
        if transkribus_base_url is None:
            transkribus_base_url = os.environ.get("TRANSKRIBUS_BASE_URL", None)
            if transkribus_base_url is None:
                raise AttributeError(
                    "Transkribus Base Url needs to be set in environment or init"
                )
        if goobi_base_url is None:
            goobi_base_url = os.environ.get("GOOBI_BASE_URL", None)
            if goobi_base_url is None:
                print("WARNING: Goobi url not set")
        self.base_url = transkribus_base_url
        self.login_cookie = self.login(user, password)
        if goobi_base_url is not None:
            self.goobi_base_url = goobi_base_url + "?id={}"
        else:
            self.goobi_base_url = None
