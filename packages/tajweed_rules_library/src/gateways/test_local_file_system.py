import unittest, os, shutil, json
from src.gateways.local_file_system import LocalFileSystem

ROOT = os.path.abspath(os.path.join(os.getcwd(), 'src'))
INPUT_FILE = os.path.join(ROOT, 'fixtures/mock_fixtures/idhaar_mock_input.txt')
ENTITIES_DIR = os.path.join(ROOT, 'entities')
OUTPUTS_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'outputs', 'specs')

FILES_SYS = {
	'root': ROOT,
	'input_file': INPUT_FILE,
	'entities_dir': ENTITIES_DIR,
	'outputs_dir': OUTPUTS_DIR
}

mock_file_system = LocalFileSystem(files_sys=FILES_SYS)
mock_file_system_with_entity = LocalFileSystem(files_sys=FILES_SYS, entity='ikhfa_shafawi')

class TestLocalFileSystem(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    if not os.path.exists(OUTPUTS_DIR):
      os.makedirs(OUTPUTS_DIR)

  @classmethod
  def tearDownClass(cls):
    if OUTPUTS_DIR:
      shutil.rmtree(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'outputs'))

  def test_get_files_in_dir(self):
    filenames = mock_file_system.get_files_in_dir()
    self.assertTrue(type(filenames), list)
    # self.assertIn('madd_6.py', filenames)
    self.assertIn('idhaar_shafawi.py', filenames)
    # self.assertIn('qalqalah.py', filenames)
    # self.assertIn('ikhfa.py', filenames)
    # self.assertIn('ghunnah.py', filenames)
    self.assertNotIn('__init__.py', filenames)
    self.assertNotIn('entities_map.py', filenames)

  def test_get_files_in_dir_for_single_entity(self):
    filenames = mock_file_system_with_entity.get_files_in_dir()
    self.assertTrue(type(filenames), list)
    self.assertEqual(len(filenames), 1)
    self.assertIn('ikhfa_shafawi.py', filenames)
    self.assertNotIn('idhaar_shafawi.py', filenames)
    self.assertNotIn('__init__.py', filenames)
    self.assertNotIn('entities_map.py', filenames)

  def test_read_entire_file_content(self):
    file_content = mock_file_system.read_file_by_lines()
    self.assertEqual(file_content[0].strip('\n'), '2|1|بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ الٓمٓ')
    self.assertEqual(file_content[len(file_content)-1].strip('/n'), '2|286|لَا يُكَلِّفُ ٱللَّهُ نَفْسًا إِلَّا وُسْعَهَا ۚ لَهَا مَا كَسَبَتْ وَعَلَيْهَا مَا ٱكْتَسَبَتْ ۗ رَبَّنَا لَا تُؤَاخِذْنَآ إِن نَّسِينَآ أَوْ أَخْطَأْنَا ۚ رَبَّنَا وَلَا تَحْمِلْ عَلَيْنَآ إِصْرًا كَمَا حَمَلْتَهُۥ عَلَى ٱلَّذِينَ مِن قَبْلِنَا ۚ رَبَّنَا وَلَا تُحَمِّلْنَا مَا لَا طَاقَةَ لَنَا بِهِۦ ۖ وَٱعْفُ عَنَّا وَٱغْفِرْ لَنَا وَٱرْحَمْنَآ ۚ أَنتَ مَوْلَىٰنَا فَٱنصُرْنَا عَلَى ٱلْقَوْمِ ٱلْكَٰفِرِينَ')

  def test_create_absolute_path(self):
    absolute_path = mock_file_system.create_absolute_output_path('test')
    self.assertEqual(os.path.join(OUTPUTS_DIR, 'test.json'), absolute_path)

  def test_write_to_file(self):
    content = {'test': 'I am some test content', }
    path = mock_file_system.create_absolute_output_path('test')
    mock_file_system.write_to_file(content, path)
    with open(os.path.join(OUTPUTS_DIR, 'test.json')) as input_file:
      entire_file = json.load(input_file)
      self.assertEqual(entire_file, content)