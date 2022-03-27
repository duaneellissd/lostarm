#! /usr/bin/python3

import os
import sys
import socket
import datetime
import getpass
import hashlib
import crcmod
import zlib
import argparse

if sys.version_info[0] != 3:
    print("This code assumes python3")
    sys.exit(1)

class bin2c():
    def __init__(self):
        self.results = dict()
        self.keys_ignored = []
        self.results["toolfile"] = os.path.abspath(__file__ )
        self.results["cwd" ] = os.getcwd()
        self.results["user"] = getpass.getuser()
        self.results["generated_date"] = datetime.datetime.now().ctime()

    def _myhash( self ):
        md5sum = hashlib.md5()

        md5sum.update(self.data)
        self.results["md5sum"] = md5sum.hexdigest()

        crc32 = crcmod.predefined.mkCrcFun("posix")
        self.results["crc32_posix"] = hex(crc32(self.data))
        self.results["crc32_zlib"] = hex(zlib.crc32( self.data ))
        crc16 = crcmod.predefined.mkCrcFun("xmodem")
        self.results["crc16_xmodem"] = hex(crc16(self.data))
        csum = 0
        xsum = 0
        for b in self.data:
            b = b & 0x0ff
            csum += b
            xsum = xsum ^ b
        self.results["csum8"] = csum & 0x0ff
        self.results["xsum8"] = xsum & 0xff

    def read_bin( self, fn ):
        data = bytearray()
        with open(fn,"rb") as f:
            data = f.read()
        self.data = data
        self.results["sizeof_binfile"] = len(self.data)
        s = os.stat( fn )
        self.results["binfile_timestamp"] = datetime.datetime.fromtimestamp( s.st_mtime )
        self._myhash()

    def open_output( self, filename ):
        self.out_fp = open( filename, "wt" )
    def close_output(self):
        if self.out_fp is not None:
            self.out_fp.close()
        self.out_fp = None

    def wr_generated_comment(self):
        self.out_fp.write("\n\n")
        # C comments incase compiler cannot handle C++ comments
        self.out_fp.write( "/* This is a generated file\n" )
        for k,v in self.results.items():
            # skip some items
            if k in self.keys_ignored:
                continue
            self.out_fp.write(" * %*s: %s\n" % (20, k,v) )
        self.out_fp.write(" */\n")


    def wr_h_body( self ):
        self.out_fp.write("\n\n")
        self.out_fp.write("#ifndef %s_INCLUDE_BLOCK\n" % self.results["var_name"])
        self.out_fp.write("#define %s_INCLUDE_BLOCK %s\n" % (self.results["var_name"], self.results["md5sum"]) )

        self.wr_extern_c()
        self.out_fp.write("\n\n\n#endif /* %s_INCLUDE_BLOCK */\n"  % self.results["var_name"])

    def wr_extern_c(self):
        self.out_fp.write("#define SIZEOF_%s %d\n" % (self.results["var_name"], len(self.data)))
        self.out_fp.write("extern\n")
        self.out_fp.write("#ifdef __cplusplus\n")
        self.out_fp.write("        \"C\"\n")
        self.out_fp.write("#endif\n")
        self.out_fp.write("                   unsigned char %s[ SIZEOF_%s ];\n" % (self.results["var_name"], self.results["var_name"]))

    def _wrbyte( self,n,b,ch ):
            if (b >= 0x20) and (b < 0x7e):
                c = ' ' + chr(b)
            else:
                if( b == 0x0a ):
                    c = "\\n"
                elif( b == 0x0d ):
                    c = "\\r"
                elif( b == 0x09 ):
                    c = "\\t"
                else:
                    c = "."
            self.out_fp.write("    0x%02x%c /* %5d | ch=%s, %3d */\n" % (b,ch,n,c,b) )
    def wr_c_body(self):
        self.out_fp.write("\n\n")
        self.out_fp.write("// #include \"%s\"\n" % self.results["h_filename"])
        self.out_fp.write("/* the H file might be stored elsewhere and have a path prefix\n")
        self.out_fp.write(" * Example: #include <generated/filename.h> might be required\n")
        self.out_fp.write(" * instead of just plain: #include \"filename.h\"\n")
        self.out_fp.write(" * So we just write the extern C here\n")
        self.out_fp.write(" */\n");
        self.wr_extern_c()
        self.out_fp.write("\n\n")
        self.out_fp.write("const unsigned char %s[ SIZEOF_%s ] = {\n" % (self.results["var_name"], self.results["var_name"]))
        dd = self.data
        for n, b in enumerate( dd[0:-1] ):
            self._wrbyte( n, b, ',')
        # last byte has no comma
        self._wrbyte( len(dd)-1, dd[-1], ' ')
        self.out_fp.write("};\n")


    def bin2c( self ):
        self.open_output( self.results['c_filename'])
        self.wr_generated_comment()
        self.wr_c_body()
        self.close_output()

    def bin2h( self ):
        self.open_output( self.results['h_filename'])
        self.wr_generated_comment()
        self.wr_h_body()
        self.close_output()


    def set_varname( self, name ):
        self.results['var_name'] = name

    def set_h_filename(self,filename):
        self.results['h_filename'] = filename

    def set_c_filename(self,filename):
        self.results['c_filename'] = filename
        

if __name__ == '__main__':
    b2c = bin2c()
    p = argparse.ArgumentParser(description="Convert Bin files to C arrays")
    p.add_argument( "binfile", type=str,help="binfilename input")
    p.add_argument( "var_name", type=str, help="help name of the variable")
    p.add_argument( "c_filename", type=str, help= "name of the C generated filename")
    args = p.parse_args()
    b2c.set_varname( args.var_name )
    if( args.c_filename[-2:] != '.c' ):
        print("ERROR: c filename must end in '.c', not %s:" % args.c_filename)
    b2c.set_c_filename( args.c_filename)
    tmp = args.c_filename[:-2] + '.h'
    b2c.set_h_filename( tmp )

    b2c.read_bin( args.binfile )
    b2c.bin2c()
    b2c.bin2h()
    sys.exit(0)
    

    
