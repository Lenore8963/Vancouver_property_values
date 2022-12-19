'''
CS5001
Final project
Fall 2022
Chen Zhou

Test Vancouver property Functions
'''


import unittest


from functions import *

class testFunctions(unittest.TestCase):

    def test_open_csv_basic(self):
        data_link1 = 'https://openhousing.ca/wp-content/uploads/2022/11/vanresales2016.csv'
        content = open_csv(data_link1)
        self.assertIsInstance(content, str)

    def test_open_csv_ValueError(self):
        with self.assertRaises(ValueError):
            open_csv(123)

    def test_open_csv_HTTPError(self):
        data_link2 = 'https://www.pipsnacks.com/404'
        with self.assertRaises(HTTPError):
            open_csv(data_link2)

    def test_create_bc_property_value_dict_basic(self):
        property_tax2016_data1 = '''PID;LEGAL_TYPE;FOLIO;LAND_COORDINATE;ZONING_DISTRICT;ZONING_CLASSIFICATION;LOT;PLAN;BLOCK;DISTRICT_LOT;FROM_CIVIC_NUMBER;TO_CIVIC_NUMBER;STREET_NAME;PROPERTY_POSTAL_CODE;NARRATIVE_LEGAL_LINE1;NARRATIVE_LEGAL_LINE2;NARRATIVE_LEGAL_LINE3;CURRENT_LAND_VALUE;CURRENT_IMPROVEMENT_VALUE;TAX_ASSESSMENT_YEAR;NARRATIVE_LEGAL_LINE4;NARRATIVE_LEGAL_LINE5;PREVIOUS_IMPROVEMENT_VALUE;PREVIOUS_LAND_VALUE;YEAR_BUILT;BIG_IMPROVEMENT_YEAR;TAX_LEVY;NEIGHBOURHOOD_CODE;REPORT_YEAR												
006-429-319;STRATA;588255490010;58825549;RM-3A;Multiple Dwelling;10;VAS1345;;184;202;2045;FRANKLIN ST;V5L 1R4;LOT 10  PLAN VAS1345  DISTRICT LOT;184  NEW WESTMINSTER UNDIV 566/1729;4 SHARE IN COM PROP THEREIN.;126000;74800;2016;;;74900;112000;1983;1983;635.66;014;2016												
015-291-600;LAND;601255290000;60125529;RT-4;Two-Family Dwelling;20;404 & 1771;19;264A;;2029;PARKER ST;V5L 2L4;LOT 20  BLOCK 19  PLAN 404 & 1771;DISTRICT LOT 264A  NEW WESTMINSTER;;1100000;34300;2016;;;24100;870000;1946;1956;4768.82;014;2016												
'''
        expect_property_value_dictionary = {'006-429-319': ['126000', '74800'], '015-291-600': ['1100000', '34300']} 
        self.assertEqual(create_bc_property_value_dict(property_tax2016_data1), expect_property_value_dictionary)

    def test_create_bc_property_value_dict_TypeError(self):
        with self.assertRaises(TypeError):
            property_tax2016_data2 = 123-456-789
            create_bc_property_value_dict(property_tax2016_data2)

    def test_create_bc_property_value_dict_IndexError(self):
        with self.assertRaises(IndexError):
            property_tax2016_data3 = '''PID;LEGAL_TYPE;FOLIO;LAND_COORDINATE;ZONING_DISTRICT;ZONING_CLASSIFICATION;LOT;PLAN;BLOCK;DISTRICT_LOT;FROM_CIVIC_NUMBER;TO_CIVIC_NUMBER;STREET_NAME;PROPERTY_POSTAL_CODE;NARRATIVE_LEGAL_LINE1;NARRATIVE_LEGAL_LINE2;NARRATIVE_LEGAL_LINE3;CURRENT_LAND_VALUE										
006-429-319;STRATA;588255490010;58825549;RM-3A;Multiple Dwelling;10;VAS1345;;184;202;2045;FRANKLIN ST;V5L 1R4;LOT 10  PLAN VAS1345  DISTRICT LOT;184  NEW WESTMINSTER UNDIV 566/1729;4 SHARE IN COM PROP THEREIN.;126000												
015-291-600;LAND;601255290000;60125529;RT-4;Two-Family Dwelling;20;404 & 1771;19;264A;;2029;PARKER ST;V5L 2L4;LOT 20  BLOCK 19  PLAN 404 & 1771;DISTRICT LOT 264A  NEW WESTMINSTER;;1100000												
'''
            create_bc_property_value_dict(property_tax2016_data3)

    def test_clean_bc_property_value_dict_basic(self):
        property_value_dictionary1 = {'006-429-319': ['$', '74800'], '015-291-600': ['1100000', '34300']}
        expect_property_value_dictionary = {'015-291-600': ['1100000', '34300']}
        self.assertEqual(clean_bc_property_value_dict(property_value_dictionary1), expect_property_value_dictionary)

    def test_clean_bc_property_value_dict_TypeError(self):
        with self.assertRaises(TypeError):
            property_value_dictionary2 = [123-456-789]
            clean_bc_property_value_dict(property_value_dictionary2)

    def test_create_bc_assessed_value_dict_basic(self):
        property_value_dictionary1 = {'006-429-319': ['126000', '74800'], '015-291-600': ['1100000', '34300']}
        expect_assessed_value_dictionary = {'006-429-319': 200800, '015-291-600': 1134300}
        self.assertEqual(create_bc_assessed_value_dict(property_value_dictionary1), expect_assessed_value_dictionary)

    def test_create_bc_assessed_value_dict_TypeError(self):
        with self.assertRaises(TypeError):
            property_value_dictionary2 = [123-456-789]
            create_bc_assessed_value_dict(property_value_dictionary2)

    def test_create_bc_assessed_value_dict_ValueError1(self):
        with self.assertRaises(ValueError):
            property_value_dictionary3 = {'006-429-319': ['$', '74800'] }
            create_bc_assessed_value_dict(property_value_dictionary3)
            
    def test_create_bc_assessed_value_dict_ValueError2(self):
        with self.assertRaises(ValueError):
            property_value_dictionary4 = {'006-429-319': ['126000', '$'] }
            create_bc_assessed_value_dict(property_value_dictionary4)

    def test_create_bc_assessed_value_dict_IndexError(self):
        with self.assertRaises(IndexError):
            property_value_dictionary5 = {'006-429-319': ['126000'] }
            create_bc_assessed_value_dict(property_value_dictionary5)

    def test_create_van_sales_list_basic(self):
        sales_data1 = '''\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n
"019-084-358","103-8460 JELLICOE ST VANCOUVER","2016-02-09","$330,000"
"005-944-112","4120 BALACLAVA ST VANCOUVER","2016-01-18","$2,159,000"
'''
        expect_sales_list = [['019-084-358', '103-8460 JELLICOE ST VANCOUVER', '09-02-2016', 330000], ['005-944-112', '4120 BALACLAVA ST VANCOUVER', '18-01-2016', 2159000]]
        self.assertEqual(create_van_sales_list(sales_data1), expect_sales_list)

    def test_create_van_sales_list_TypeError(self):
        with self.assertRaises(TypeError):
            sales_data2 = [123-456-789]
            create_van_sales_list(sales_data2)

    def test_create_van_sales_list_ValueError1(self):
        with self.assertRaises(ValueError):
            sales_data3 = '''\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n
"019-084-358","103-8460 JELLICOE ST VANCOUVER","???","$330,000"
'''
            create_van_sales_list(sales_data3)            

    def test_create_van_sales_list_ValueError2(self):
        with self.assertRaises(ValueError):
            sales_data4 = '''\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n
"005-944-112","4120 BALACLAVA ST VANCOUVER","2016-01-18","$$$"
'''
            create_van_sales_list(sales_data4)

    def test_create_van_sales_list_IndexError(self):
        with self.assertRaises(IndexError):
            sales_data5 = '''\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n
"005-944-112","4120 BALACLAVA ST VANCOUVER","2016-01-18"
'''
            create_van_sales_list(sales_data5)

    def test_create_sales_records_dict_basic(self):
        sales_list1 = [['019-084-358', '103-8460 JELLICOE ST VANCOUVER', '09-02-2016', 330000], ['005-944-112', '4120 BALACLAVA ST VANCOUVER', '18-01-2016', 2159000], ['019-084-358', '103-8460 JELLICOE ST VANCOUVER', '17-05-2016', 450000]]
        expect_sales_record_dictionary = {'019-084-358': [['09-02-2016', 330000], ['17-05-2016', 450000]], '005-944-112': [['18-01-2016', 2159000]]}
        self.assertEqual(create_sales_records_dict(sales_list1), expect_sales_record_dictionary)

    def test_create_sales_records_dict_TypeError(self):
        with self.assertRaises(TypeError):
            sales_list2 = '123-456-789'
            create_sales_records_dict(sales_list2)

    def test_create_sales_records_dict_IndexError(self):
        with self.assertRaises(IndexError):
            sales_list3 = [['019-084-358', '103-8460 JELLICOE ST VANCOUVER', '09-02-2016']]
            create_sales_records_dict(sales_list3)

    def test_clean_sales_records_dict_basic(self):
        sales_record_dictionary1 = {'019-084-358': [ ['17-05-2016', 450000], ['09-02-2016', 330000], ['09-02-2016', 330000]], '005-944-112': [['18-01-2016', 2159000], ['18-01-2016', 2159000]]}
        expect_sales_record_dictionary = {'019-084-358': [['09-02-2016', 330000], ['17-05-2016', 450000]], '005-944-112': [['18-01-2016', 2159000]]}
        self.assertEqual(clean_sales_records_dict(sales_record_dictionary1), expect_sales_record_dictionary)

    def test_clean_sales_records_dict_TypeError(self):
        with self.assertRaises(TypeError):
            sales_list2 = '123-456-789'
            clean_sales_records_dict(sales_list2)

    def test_create_van_property_dict_basic(self):
        assessed_value_dictionary1 = {'019-084-358': 400000, '006-429-319': 200800, '015-291-600': 1134300}
        sales_list1 = [['019-084-358', '103-8460 JELLICOE ST VANCOUVER', '09-02-2016', 330000], ['005-944-112', '4120 BALACLAVA ST VANCOUVER', '18-01-2016', 2159000]]
        expect_property_dictionary = {'019-084-358': [400000, '103-8460 JELLICOE ST VANCOUVER']}
        self.assertEqual(create_van_property_dict(assessed_value_dictionary1, sales_list1), expect_property_dictionary)

    def test_create_van_property_dict_TypeError1(self):
        with self.assertRaises(TypeError):
            assessed_value_dictionary2 = '123-456-789'
            sales_list2 = [['019-084-358', '103-8460 JELLICOE ST VANCOUVER', '09-02-2016', 330000]]
            create_van_property_dict(assessed_value_dictionary2, sales_list2)

    def test_create_van_property_dict_TypeError2(self):
        with self.assertRaises(TypeError):
            assessed_value_dictionary3 = {'019-084-358': 400000}
            sales_list3 = '019-084-358'
            create_van_property_dict(assessed_value_dictionary3, sales_list3)

    def test_create_van_property_dict_IndexError(self):
        with self.assertRaises(IndexError):
            assessed_value_dictionary4 = {'019-084-358': 400000}
            sales_list4 = [['019-084-358']]
            create_van_property_dict(assessed_value_dictionary4, sales_list4)

    def test_add_property_data_into_class_basic(self):
        property_dictionary1 = {'019-084-358': [400000, '103-8460 JELLICOE ST VANCOUVER']}
        expect_property_class = {'019-084-358': Property('019-084-358', 400000, '103-8460 JELLICOE ST VANCOUVER')}
        self.assertEqual(add_property_data_into_class(property_dictionary1), expect_property_class)

    def test_add_property_data_into_class_TypeError(self):
        with self.assertRaises(TypeError):
            property_dictionary2 = '123-456-789'
            add_property_data_into_class(property_dictionary2)

    def test_add_sales_data_into_class_basic(self):
        sales_record_dictionary1 = {'019-084-358': [['09-02-2016', 330000], ['17-05-2016', 450000]], '005-944-112': [['18-01-2016', 2159000]]}
        expect_sales_class = {'019-084-358': SalesEvent('019-084-358', [['09-02-2016', 330000], ['17-05-2016', 450000]], 450000), '005-944-112': SalesEvent('005-944-112', [['18-01-2016', 2159000]], 2159000)}
        self.assertEqual(add_sales_data_into_class(sales_record_dictionary1), expect_sales_class)

    def test_add_sales_data_into_class_TypeError(self):
        with self.assertRaises(TypeError):
            sales_record_dictionary2 = ['123-456-789']
            add_sales_data_into_class(sales_record_dictionary2)

    def test_add_sales_data_into_class_IndexError(self):
        with self.assertRaises(IndexError):
            sales_record_dictionary3 = {'019-084-358': [['09-02-2016']]}
            add_sales_data_into_class(sales_record_dictionary3)

    def test_count_number_of_sales_basic(self):
        sales_class1 = {'019-084-358': SalesEvent('019-084-358', [['09-02-2016', 330000], ['17-05-2016', 450000]], 450000), '005-944-112': SalesEvent('005-944-112', [['18-01-2016', 2159000]], 2159000)}
        expect_sales_statistics = {'one_time': 1, 'twice': 1}
        self.assertEqual(count_number_of_sales(sales_class1), expect_sales_statistics)

    def test_count_number_of_sales_TypeError1(self):
        with self.assertRaises(TypeError):
            sales_class2 = '123-456-789'
            count_number_of_sales(sales_class2)

    def test_count_number_of_sales_TypeError2(self):
        with self.assertRaises(TypeError):
            sales_class3 = {'019-084-358': [['09-02-2016', 330000], ['17-05-2016', 450000]]}
            count_number_of_sales(sales_class3)

    def test_create_sales_and_assessed_price_list_basic(self):
        propertry_class1 = {'019-084-358': Property('019-084-358', 400000, '103-8460 JELLICOE ST VANCOUVER'), '005-944-112': Property('005-944-112', 2159000, '4120 BALACLAVA ST VANCOUVER')}
        sales_class1 = {'019-084-358': SalesEvent('019-084-358', [['09-02-2016', 330000], ['17-05-2016', 450000]], 450000)}
        expect_sales_and_assessed_list = [['019-084-358', 330000, 400000], ['019-084-358', 450000, 400000]]
        self.assertEqual(create_sales_and_assessed_price_list(propertry_class1, sales_class1), expect_sales_and_assessed_list)

    def test_create_sales_and_assessed_price_list_TypeError1(self):
        with self.assertRaises(TypeError):
            propertry_class2 = ['123-456-789']
            sales_class2 = {'019-084-358': SalesEvent('019-084-358', [['09-02-2016', 330000], ['17-05-2016', 450000]], 450000)}
            create_sales_and_assessed_price_list(propertry_class2, sales_class2)

    def test_create_sales_and_assessed_price_list_TypeError2(self):
        with self.assertRaises(TypeError):
            propertry_class3 = {'019-084-358': Property('019-084-358', 400000, '103-8460 JELLICOE ST VANCOUVER')}
            sales_class3 = ['123-456-789']
            create_sales_and_assessed_price_list(propertry_class3, sales_class3)

    def test_create_sales_and_assessed_price_list_TypeError3(self):
        with self.assertRaises(TypeError):
            propertry_class4 = {'019-084-358': [400000, '103-8460 JELLICOE ST VANCOUVER']}
            sales_class4 = {'019-084-358': SalesEvent('019-084-358', [['09-02-2016', 330000], ['17-05-2016', 450000]], 450000)}
            create_sales_and_assessed_price_list(propertry_class4, sales_class4)

    def test_create_sales_and_assessed_price_list_TypeError4(self):
        with self.assertRaises(TypeError):
            propertry_class5 = {'019-084-358': Property('019-084-358', 400000, '103-8460 JELLICOE ST VANCOUVER')}
            sales_class5 = {'019-084-358': [['09-02-2016', 330000], ['17-05-2016', 450000]]}
            create_sales_and_assessed_price_list(propertry_class5, sales_class5)

    def test_create_sales_and_assessed_price_list_IndexError(self):
        with self.assertRaises(IndexError):
            propertry_class6 = {'019-084-358': Property('019-084-358', 400000, '103-8460 JELLICOE ST VANCOUVER')}
            sales_class6 = {'019-084-358': SalesEvent('019-084-358', [['09-02-2016'], ['17-05-2016', 450000]], 450000)}
            create_sales_and_assessed_price_list(propertry_class6, sales_class6)

    def test_calculate_sar_list_basic(self):
        sales_and_assessed_list1 = [['019-084-358', 330000, 300000], ['019-084-358', 460000, 300000], ['005-944-112', 2159000, 2000000]]
        expect_sar_list = [['019-084-358', 330000, 300000, 1.100], ['019-084-358', 460000, 300000, 1.533], ['005-944-112', 2159000, 2000000, 1.079]]
        self.assertEqual(calculate_sar_list(sales_and_assessed_list1), expect_sar_list)

    def test_calculate_sar_list_TypeError(self):
        with self.assertRaises(TypeError):
            sales_and_assessed_list2 = {'019-084-358': 300000}
            calculate_sar_list(sales_and_assessed_list2)

    def test_calculate_sar_list_ValueError1(self):
        with self.assertRaises(ValueError):
            sales_and_assessed_list3 = [['019-084-358', '$', 300000]]
            calculate_sar_list(sales_and_assessed_list3)

    def test_calculate_sar_list_ValueError2(self):
        with self.assertRaises(ValueError):
            sales_and_assessed_list4 = [['019-084-358', 330000, '$']]
            calculate_sar_list(sales_and_assessed_list4)

    def test_calculate_sar_list_ZeroDivisionError(self):
        with self.assertRaises(ZeroDivisionError):
            sales_and_assessed_list5 = [['019-084-358', 330000, 0]]
            calculate_sar_list(sales_and_assessed_list5)

    def test_calculate_sar_list_IndexError(self):
        with self.assertRaises(IndexError):
            sales_and_assessed_list6 = [['019-084-358', 330000]]
            calculate_sar_list(sales_and_assessed_list6)

    def test_create_big_improvement_list_basic(self):
        property_tax2018_data1 = '''PID;LEGAL_TYPE;FOLIO;LAND_COORDINATE;ZONING_DISTRICT;ZONING_CLASSIFICATION;LOT;PLAN;BLOCK;DISTRICT_LOT;FROM_CIVIC_NUMBER;TO_CIVIC_NUMBER;STREET_NAME;PROPERTY_POSTAL_CODE;NARRATIVE_LEGAL_LINE1;NARRATIVE_LEGAL_LINE2;NARRATIVE_LEGAL_LINE3;CURRENT_LAND_VALUE;CURRENT_IMPROVEMENT_VALUE;TAX_ASSESSMENT_YEAR;NARRATIVE_LEGAL_LINE4;NARRATIVE_LEGAL_LINE5;PREVIOUS_IMPROVEMENT_VALUE;PREVIOUS_LAND_VALUE;YEAR_BUILT;BIG_IMPROVEMENT_YEAR;TAX_LEVY;NEIGHBOURHOOD_CODE;REPORT_YEAR								
029-848-199;STRATA;138600890239;13860089;CD-1 (525);Comprehensive Development;239;EPS3242;54;541;2902;777;RICHARDS ST;V6B 0M6;LOT 239  BLOCK 54  PLAN EPS3242  DI;STRICT LOT 541  NWD GROUP 1	 TOGETH;ER WITH AN INTEREST IN THE COMMON P;467000;243000;2018;ROPERTY IN PROPORTION TO THE UNIT E;NTITLEMENT OF THE STRATA LOT AS SHO;243000;371000;2016;2016;1752.47;026;2018							
029-777-852;STRATA;184638960051;18463896;CD-1 (506);Comprehensive Development;51;EPS2426;;200A;804;1788;ONTARIO ST;V5T 0G3;LOT 51  PLAN EPS2426  DISTRICT LOT;200A  NWD GROUP 1	 TOGETHER WITH AN;INTEREST IN THE COMMON PROPERTY IN;455000;172000;2018;PROPORTION TO THE UNIT ENTITLEMENT;OF THE STRATA LOT AS SHOWN ON FORM;172000;371000;2016;2016;1549.32;013;2018
027-639-240;STRATA;686149060010;68614906;RM-3;Multiple Dwelling;10;BCS3082;;526;301;1088;14TH AVE W;V6H 0A6;LOT 10  PLAN BCS3082  DISTRICT LOT;526  NWD GROUP 1	 TOGETHER WITH AN;INTEREST IN THE COMMON PROPERTY IN;594000;238000;2018;PROPORTION TO THE UNIT.;;241000;474000;2008;2008;2053.58;007;2018											
'''							
        expect_big_improvement_list = ['029-848-199', '029-777-852']
        self.assertEqual(create_big_improvement_list(property_tax2018_data1), expect_big_improvement_list)

    def test_create_big_improvement_list_TypeError(self):
        with self.assertRaises(TypeError):
            property_tax2018_data2 = 123-456-789
            create_big_improvement_list(property_tax2018_data2)

    def test_create_big_improvement_list_IndexError(self):
        with self.assertRaises(IndexError):
            property_tax2018_data3 = '''PID;LEGAL_TYPE;FOLIO;LAND_COORDINATE;ZONING_DISTRICT;ZONING_CLASSIFICATION;LOT;PLAN;BLOCK;DISTRICT_LOT;FROM_CIVIC_NUMBER;TO_CIVIC_NUMBER;STREET_NAME;PROPERTY_POSTAL_CODE;NARRATIVE_LEGAL_LINE1;NARRATIVE_LEGAL_LINE2;NARRATIVE_LEGAL_LINE3;CURRENT_LAND_VALUE;CURRENT_IMPROVEMENT_VALUE;TAX_ASSESSMENT_YEAR;NARRATIVE_LEGAL_LINE4;NARRATIVE_LEGAL_LINE5;PREVIOUS_IMPROVEMENT_VALUE;PREVIOUS_LAND_VALUE;YEAR_BUILT
029-848-199;STRATA;138600890239;13860089;CD-1 (525);Comprehensive Development;239;EPS3242;54;541;2902;777;RICHARDS ST;V6B 0M6;LOT 239  BLOCK 54  PLAN EPS3242  DI;STRICT LOT 541  NWD GROUP 1	 TOGETH;ER WITH AN INTEREST IN THE COMMON P;467000;243000;2018;ROPERTY IN PROPORTION TO THE UNIT E;NTITLEMENT OF THE STRATA LOT AS SHO;243000;371000;2016
029-777-852;STRATA;184638960051;18463896;CD-1 (506);Comprehensive Development;51;EPS2426;;200A;804;1788;ONTARIO ST;V5T 0G3;LOT 51  PLAN EPS2426  DISTRICT LOT;200A  NWD GROUP 1	 TOGETHER WITH AN;INTEREST IN THE COMMON PROPERTY IN;455000;172000;2018;PROPORTION TO THE UNIT ENTITLEMENT;OF THE STRATA LOT AS SHOWN ON FORM;172000;371000;2016
027-639-240;STRATA;686149060010;68614906;RM-3;Multiple Dwelling;10;BCS3082;;526;301;1088;14TH AVE W;V6H 0A6;LOT 10  PLAN BCS3082  DISTRICT LOT;526  NWD GROUP 1	 TOGETHER WITH AN;INTEREST IN THE COMMON PROPERTY IN;594000;238000;2018;PROPORTION TO THE UNIT.;;241000;474000;2008;2008;2053.58;007;2018											
'''			
            create_big_improvement_list(property_tax2018_data3)

    def sar_list_without_big_improvement(self):
        sar_list1 = [['019-084-358', 330000, 300000, 1.100], ['005-944-112', 2159000, 2000000, 1.079]]				
        big_improvement_list1 = ['005-944-112', '029-777-852']
        expect_new_sar_list = [['019-084-358', 330000, 300000, 1.100]]
        self.assertEqual(sar_list_without_big_improvement(sar_list1, big_improvement_list1), expect_new_sar_list)

    def test_sar_list_without_big_improvement_TypeError1(self):
        with self.assertRaises(TypeError):
            sar_list2 = {'019-084-358': 330000}				
            big_improvement_list2 = ['005-944-112', '029-777-852']
            sar_list_without_big_improvement(sar_list2, big_improvement_list2)

    def test_sar_list_without_big_improvement_TypeError2(self):
        with self.assertRaises(TypeError):
            sar_list3 = [['019-084-358', 330000, 300000, 1.100], ['005-944-112', 2159000, 2000000, 1.079]]				
            big_improvement_list3 = '005-944-112'
            sar_list_without_big_improvement(sar_list3, big_improvement_list3)

    def test_sar_list_without_big_improvement_TypeError3(self):
        with self.assertRaises(TypeError):
            sar_list4 = [['019-084-358', 330000, 300000, '1.100'], ['005-944-112', 2159000, 2000000, 1.079]]				
            big_improvement_list4 = ['005-944-112', '029-777-852']
            sar_list_without_big_improvement(sar_list4, big_improvement_list4)

    def test_sar_list_without_big_improvement_IndexError(self):
        with self.assertRaises(IndexError):
            sar_list5 = [['019-084-358', 330000, 300000], ['005-944-112', 2159000, 2000000, 1.079]]				
            big_improvement_list5 = ['005-944-112', '029-777-852']
            sar_list_without_big_improvement(sar_list5, big_improvement_list5)

    def test_count_sar_dict_basic(self):
        new_sar_list1 = [['019-084-358', 330000, 300000, 1.100], ['019-084-358', 460000, 300000, 1.533], ['005-944-112', 2159000, 2000000, 1.079]]				
        expect_sar_dictionary = {'< 1.0': 0, '1.0 - 1.25': 2, '1.25 - 1.5': 0, '> 1.5': 1}
        self.assertEqual(count_sar_dict(new_sar_list1), expect_sar_dictionary)

    def test_count_sar_dict_TypeError1(self):
        with self.assertRaises(TypeError):
            new_sar_list2 = {'019-084-358': 330000}				
            count_sar_dict(new_sar_list2)

    def test_count_sar_dict_TypeError2(self):
        with self.assertRaises(TypeError):
            new_sar_list3 = [['019-084-358', 330000, 300000, '1.100'], ['005-944-112', 2159000, 2000000, '1.079']]				
            count_sar_dict(new_sar_list3)

    def test_count_sar_dict_IndexError(self):
        with self.assertRaises(IndexError):
            new_sar_list4 = [['019-084-358', 330000, 300000], ['005-944-112', 2159000, 2000000, 1.079]]				
            count_sar_dict(new_sar_list4)

    def test_rank_sar_list_basic(self):
        new_sar_list1 = [['019-084-358', 330000, 300000, 1.100], ['019-084-358', 460000, 300000, 1.533], ['005-944-112', 2159000, 2000000, 1.079]]				
        expect_sorted_list = [['019-084-358', 460000, 300000, 1.533], ['019-084-358', 330000, 300000, 1.100], ['005-944-112', 2159000, 2000000, 1.079]]
        self.assertEqual(rank_sar_list(new_sar_list1), expect_sorted_list)

    def test_rank_sar_list_TypeError(self):
        with self.assertRaises(TypeError):
            new_sar_list2 = {'019-084-358': 330000}				
            rank_sar_list(new_sar_list2)

    def test_rank_sar_list_ValueError(self):
        with self.assertRaises(ValueError):
            new_sar_list3 = [['019-084-358', 330000, 300000, '$'], ['005-944-112', 2159000, 2000000, '#']]				
            rank_sar_list(new_sar_list3)

    def test_rank_sar_list_IndexError(self):
        with self.assertRaises(IndexError):
            new_sar_list4 = [['019-084-358', 330000, 300000], ['005-944-112', 2159000, 2000000]]				
            rank_sar_list(new_sar_list4)


def main():

     unittest.main(verbosity = 3)


if __name__ == "__main__":
    main()
