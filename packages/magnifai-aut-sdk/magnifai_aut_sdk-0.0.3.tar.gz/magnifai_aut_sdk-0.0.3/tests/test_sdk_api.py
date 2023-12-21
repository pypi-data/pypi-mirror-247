import json

from magnifai_aut_sdk.aut_properties import AutProperties
from magnifai_aut_sdk.magnifai import Magnifai

EXECUTION = "64f720e2369a3e455f228d03"
AutProperties.load_property_file('config.ini')


def test_compare():
    excluded_areas = [
            {"topLeftX": 710, "topLeftY": 150, "bottomRightX": 830, "bottomRightY": 310},
            {"topLeftX": 200, "topLeftY": 300, "bottomRightX": 500, "bottomRightY": 450}
    ]

    rs = Magnifai.compare(execution_id=EXECUTION, test_name='test magnifai-aut-magnifai_aut_sdk-python compare',
                          baseline_image='tests/images/magnifai_base.png',
                          input_image='tests/images/magnifai_input.png',
                          min_similarity='90', excluded_areas=excluded_areas)
    assert rs.status_code == 200
    response_json = json.loads(rs.text)
    assert response_json.get('status') == 'Passed'


def test_compare_url():
    rs = Magnifai.compare(execution_id=EXECUTION, test_name='test magnifai-aut-magnifai_aut_sdk-python compare urls',
                          baseline_image_url="https://upload.wikimedia.org/wikipedia/commons/b/b1/Mandriva_2009.1_KDE4.2_Bureau.png",
                          input_image_url="https://upload.wikimedia.org/wikipedia/commons/b/b1/Mandriva_2009.1_KDE4.2_Bureau.png",
                          min_similarity='90')
    assert rs.status_code == 200
    response_json = json.loads(rs.text)
    assert response_json.get('status') == 'Passed'


def test_flex_compare():
    rs = Magnifai.compare(execution_id=EXECUTION, test_name='test magnifai-aut-magnifai_aut_sdk-python flex compare',
                          baseline_image='tests/images/magnifai_base.png',
                          input_image='tests/images/magnifai_input.png', min_similarity='90')
    assert rs.status_code == 200
    response_json = json.loads(rs.text)
    assert response_json.get('status') == 'Passed'


def test_flex_compare_url():
    rs = Magnifai.flex_compare(execution_id=EXECUTION, test_name='test magnifai-aut-magnifai_aut_sdk-python flex compare url',
                               baseline_image_url="https://upload.wikimedia.org/wikipedia/commons/b/b1/Mandriva_2009.1_KDE4.2_Bureau.png",
                               input_image_url="https://upload.wikimedia.org/wikipedia/commons/b/b1/Mandriva_2009.1_KDE4.2_Bureau.png",
                               min_similarity='90')
    assert rs.status_code == 200
    response_json = json.loads(rs.text)
    assert response_json.get('status') == 'Passed'


def test_search():
    rs = Magnifai.search(execution_id=EXECUTION, test_name='test magnifai-aut-magnifai_aut_sdk-python search',
                         parent_image='tests/images/magnifai_base.png',
                         child_image='tests/images/magnifai_child.png', min_similarity='90')
    assert rs.status_code == 200
    response_json = json.loads(rs.text)
    assert response_json.get('status') == 'Found'


def test_search_url():
    rs = Magnifai.search(execution_id=EXECUTION, test_name='test magnifai-aut-magnifai_aut_sdk-python search urls',
                         parent_image_url="https://upload.wikimedia.org/wikipedia/commons/b/b1/Mandriva_2009.1_KDE4.2_Bureau.png",
                         child_image_url="https://upload.wikimedia.org/wikipedia/commons/b/b1/Mandriva_2009.1_KDE4.2_Bureau.png",
                         min_similarity='90')
    assert rs.status_code == 200
    response_json = json.loads(rs.text)
    assert response_json.get('status') == 'Found'


def test_flex_search():
    rs = Magnifai.flex_search(execution_id=EXECUTION, test_name='test magnifai-aut-magnifai_aut_sdk-python search',
                              parent_image='tests/images/magnifai_base.png',
                              child_image='tests/images/magnifai_child.png', min_similarity='90')
    assert rs.status_code == 200
    response_json = json.loads(rs.text)
    assert response_json.get('status') == 'Found'


def test_flex_search_url():
    rs = Magnifai.flex_search(execution_id=EXECUTION, test_name='test magnifai-aut-magnifai_aut_sdk-python search urls',
                              parent_image_url="https://upload.wikimedia.org/wikipedia/commons/b/b1/Mandriva_2009.1_KDE4.2_Bureau.png",
                              child_image_url="https://upload.wikimedia.org/wikipedia/commons/b/b1/Mandriva_2009.1_KDE4.2_Bureau.png",
                              min_similarity='90')
    assert rs.status_code == 200
    response_json = json.loads(rs.text)
    assert response_json.get('status') == 'Found'


def test_locate():
    rs = Magnifai.locate(execution_id=EXECUTION, test_name='test magnifai-aut-magnifai_aut_sdk-python search',
                         container_image='tests/images/magnifai_base.png',
                         main_image='tests/images/magnifai_main.png',
                         relative_image="tests/images/magnifai_relative.png",
                         min_similarity='90')
    assert rs.status_code == 200
    response_json = json.loads(rs.text)
    assert response_json.get('status') == 'Found'


def test_locate_url():
    rs = Magnifai.locate(execution_id=EXECUTION, test_name='test magnifai-aut-magnifai_aut_sdk-python search urls',
                         container_image_url="https://upload.wikimedia.org/wikipedia/commons/b/b1/Mandriva_2009.1_KDE4.2_Bureau.png",
                         main_image_url="https://upload.wikimedia.org/wikipedia/commons/b/b1/Mandriva_2009.1_KDE4.2_Bureau.png",
                         relative_image_url="https://upload.wikimedia.org/wikipedia/commons/b/b1/Mandriva_2009.1_KDE4.2_Bureau.png",
                         min_similarity='90')
    assert rs.status_code == 200
    response_json = json.loads(rs.text)
    assert response_json.get('status') == 'Found'


def test_flex_locate():
    rs = Magnifai.flex_locate(execution_id=EXECUTION, test_name='test magnifai-aut-magnifai_aut_sdk-python search',
                              container_image='tests/images/magnifai_base.png',
                              main_image='tests/images/magnifai_main.png',
                              relative_image="tests/images/magnifai_relative.png", min_similarity='90')
    assert rs.status_code == 200
    response_json = json.loads(rs.text)
    assert response_json.get('status') == 'Found'


def test_flex_locate_url():
    rs = Magnifai.flex_locate(execution_id=EXECUTION, test_name='test magnifai-aut-magnifai_aut_sdk-python search urls',
                              container_image_url="https://upload.wikimedia.org/wikipedia/commons/b/b1/Mandriva_2009.1_KDE4.2_Bureau.png",
                              main_image_url="https://upload.wikimedia.org/wikipedia/commons/b/b1/Mandriva_2009.1_KDE4.2_Bureau.png",
                              relative_image_url="https://upload.wikimedia.org/wikipedia/commons/b/b1/Mandriva_2009.1_KDE4.2_Bureau.png",
                              min_similarity='90')
    assert rs.status_code == 200
    response_json = json.loads(rs.text)
    assert response_json.get('status') == 'Found'
