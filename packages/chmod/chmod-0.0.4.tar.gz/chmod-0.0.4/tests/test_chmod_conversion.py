import pytest
from chmod import ChmodConversion
class TestChmodConversion():
    
    
    def test_octal_to_symbolic(self):
        # Test converting octal permissions to symbolic permissions
        a = ChmodConversion()
        assert a.int_to_perm(755) == "rwxr-xr-x"
        assert a.int_to_perm(644) == "rw-r--r--"
        assert a.int_to_perm(777) == "rwxrwxrwx"
        assert a.int_to_perm(771) == "rwxrwx--x"
    
    def test_symbolic_to_octal(self):
        # Test converting symbolic permissions to octal permissions
        a = ChmodConversion()
        assert a.perm_to_int("rwxr-xr-x") == 755
        assert a.perm_to_int("rw-r--r--") == 644
        assert a.perm_to_int("rwxrwxrwx") == 777
        assert a.perm_to_int("--x---rwx") == 107

if __name__ == '__main__':
    pytest.main()
