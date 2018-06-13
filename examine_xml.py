from xml.etree import ElementTree as xtree
from io import BytesIO

import os

smoking_test = os.path.join("smoking_status_data",
                            "smokers_surrogate_test_all_groundtruth_version2",
                            "smokers_surrogate_test_all_groundtruth_version2.xml")
smoking_train = os.path.join("smoking_status_data",
                             "smokers_surrogate_train_all_version2",
                             "smokers_surrogate_train_all_version2.xml")


def format_xml(train_filename, test_filename, outfolder):
    if not os.path.exists(outfolder):
        os.makedirs(outfolder)
    dataset = {}
    train_root = xtree.parse(train_filename).getroot()
    test_root = xtree.parse(test_filename).getroot()
    train_document = xtree.Element('Dataset', {'databaseroot': './',
                                              'name': 'emr-vis-nlp_smoking_status',
                                              'type': 'datasetsmoking'})

    test_document = xtree.Element('Dataset', {'databaseroot': './',
                                              'name': 'emr-vis-nlp_smoking_status',
                                              'type': 'datasetsmoking'})

    all_document = xtree.Element('Dataset', {'databaseroot': './',
                                             'name': 'emr-vis-nlp_smoking_status',
                                             'type': 'datasetsmoking'})

    dataset["train"] = [train_root, train_document, "feedbackIDList.xml"]
    dataset["test"] = [test_root, test_document, "testIDList.xml"]
    dataset["all"] = [None, all_document, "fullIDList.xml"]
    if not os.path.exists(os.path.join(outfolder, "labels")):
        os.makedirs(os.path.join(outfolder, "labels"))
    smoking_status = ["SMOKER", "CURRENT SMOKER", "PAST SMOKER", "NON-SMOKER", "UNKNOWN"]
    with open(os.path.join(outfolder, "labels", "class-smokingstatus.csv"), "w") as labels_file:
        #labels_file.write(",[classLabel]")
        labels_file.write(",[classLabel]\n")
        for each in ["train", "test"]:
            for record in dataset[each][0]:
                docID = record.get("ID")
                if len(docID) < 4:
                    docID = "2000"[:4-len(docID)] + docID
                elif len(docID) == 4:
                    docID = "3" + docID[1:]
                print(docID)
                text = record.find("TEXT").text
                status = record.find("SMOKING").get("STATUS")
                labels_file.write("{},{}\n".format(docID, smoking_status.index(status)))
                node = xtree.SubElement(dataset[each][1], "Document")
                node.text = docID
                all_node = xtree.SubElement(dataset["all"][1], "Document")
                all_node.text = docID
                if not os.path.exists(os.path.join(outfolder, "docs", docID)):
                    os.makedirs(os.path.join(outfolder, "docs", docID))
                with open(os.path.join(outfolder, "docs", docID, "report.txt"), "w") as f:
                    f.write(text)
    for each in dataset:
        if not os.path.exists(os.path.join(outfolder, "documentList")):
            os.makedirs(os.path.join(outfolder, "documentList"))
        with open(os.path.join(outfolder, "documentList", dataset[each][2]), "wb") as f:
            et = xtree.ElementTree(dataset[each][1])
            et.write(f, encoding='utf-8', xml_declaration=True)


format_xml(smoking_train, smoking_test,
           os.path.join("formatted_data", "smoking_data"))
