import unittest   # The test framework
from api_analyzer import ApiAnalyzer

data = ['/auth/token']
analyzer = ApiAnalyzer(data)

class Test_TestAntiPatterns(unittest.TestCase):
    # This test is designed for patterns
    def test_Amorphous(self):
        data = ['/user_Auth/token']
        ap, p, p_count, ap_count = analyzer.detect_amorphous_uri(data)
        self.assertEqual(ap_count, 1)

    # This test is designed for anti-pattern
    def test_nonAmorphous(self):
        data = ['aUth/tokenjpg']
        ap, p, p_count, ap_count = analyzer.detect_amorphous_uri(data)
        self.assertEqual(p_count, 1)

    #This test is designed for pattern
    def test_StandardURIs(self):
        data = ['/devices/thermostats/device_id/device_id']
        ap, p, p_count, ap_count = analyzer.detect_non_standard_uri(data)
        self.assertEqual(p_count, 1)

    #This test is designed for pattern
    def test_NonStandardURIs(self):
        data = ['/account$/set_profile_photo%']
        ap, p, p_count, ap_count = analyzer.detect_non_standard_uri(data)
        self.assertEqual(ap_count, 1)

    
    #This test is designed for pattern
    def test_nonCRUDyURI(self):
        data = ['/account/set_profile_photo']
        ap, p, p_count, ap_count = analyzer.detect_crudy_uri(data)
        self.assertEqual(p_count, 1)
    
    #This test is designedfor anti-pattern
    def test_CRUDY_URI(self):
        data = ['/account/delete']
        ap, p, p_count, ap_count = analyzer.detect_crudy_uri(data)
        self.assertEqual(ap_count, 1)
    
    #This test is designed for pattern
    def test_versionedURI(self):
        data = ['/v18.10/{album-id}']
        ap, p, p_count, ap_count = analyzer.detect_unversioned_uris(data)
        #print(ap)
        #print(p)
        self.assertEqual(p_count, 1)
    
    #This test is designedfor anti-pattern
    def test_UnversionedURIs(self):
        data = ['/contacts/delete_manual_contacts']
        ap, p, p_count, ap_count = analyzer.detect_unversioned_uris(data)
        self.assertEqual(ap_count, 1)

    #This test is designed for pattern
    def test_NonPluralisedNodes(self):
        data = ['POST>>/flows']
        ap, p, p_count, ap_count = analyzer.detect_pluralized_node(data)
        self.assertEqual(p_count, 1)
    
    #This test is designedfor anti-pattern
    def test_PluralisedNodes(self):
        data = ['POST>>/auth/token']
        ap, p, p_count, ap_count = analyzer.detect_pluralized_node(data)
        self.assertEqual(ap_count, 1)


    #This test is designed for anti pattern
    def test_descriptiveURI(self):
        data = ['/app/app_link_hosts']
        ap, p, p_count, ap_count = analyzer.detect_non_descriptive_uri(data)
        self.assertEqual(p_count,1)

    #This test is designed for anti pattern
    def test_Non_descriptiveURI(self):
        data = ['/{business_id}/owned_app']
        ap, p, p_count, ap_count = analyzer.detect_non_descriptive_uri(data)
        self.assertEqual(ap_count,1)
    
    #This test is designed for anti pattern
    def test_ContextualURI(self):
        data = ["POST >> /account/set_profile_photo >> Sets a user's profile photo."]
        ap, p, p_count, ap_count = analyzer.detect_contextless(data)
        self.assertEqual(p_count,1)

    #This test is designed for anti pattern
    def test_ContextlessURI(self):
        data = ['POST >> /auth/person >> count number of images']
        ap, p, p_count, ap_count = analyzer.detect_contextless(data)
        self.assertEqual(ap_count,1)
    
    #This test is designed for anti pattern
    def test_HierarchicalNodes(self):
        data = ["/auth/token/revoke"]
        ap, p, p_count, ap_count = analyzer.detect_non_hierarchical_nodes(data)
        self.assertEqual(p_count,1)

    #This test is designed for anti pattern
    def test_NonHierarchicalNodes(self):
        data = ['/files/move_batch/check_v2']
        ap, p, p_count, ap_count = analyzer.detect_non_hierarchical_nodes(data)
        self.assertEqual(ap_count,1)

    #This test is designed for anti pattern
    def test_CohisiveDocumentation(self):
        data = ["POST >> /account/set_profile_photo >> Sets a user's profile photo."]
        ap, p, p_count, ap_count = analyzer.detect_less_cohesive_documentation(data)
        self.assertEqual(p_count,1)

    #This test is designed for anti pattern
    def test_LessCohisiveDocumentation(self):
        data = ['POST >> /auth/person >> count number of images']
        ap, p, p_count, ap_count = analyzer.detect_less_cohesive_documentation(data)
        self.assertEqual(ap_count, 1)
    

    #This test is designed for anti pattern
    def test_ConsistantDocumentation(self):
        data = ["POST >> /account/set_profile_photo >> Sets a user's profile photo."]
        ap, p, p_count, ap_count = analyzer.detect_inconsistent_documentations(data)
        self.assertEqual(p_count,1)

    #This test is designed for anti pattern
    def test_InconsistantDocumentation(self):
        data = ['POST>>/shop/admin/variants/update_stock>>Update Variants stock']
        ap, p, p_count, ap_count = analyzer.detect_inconsistent_documentations(data)
        self.assertEqual(ap_count,1)
    

    
    
        

    


    
