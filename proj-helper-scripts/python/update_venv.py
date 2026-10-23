    def _update_activate_script(self):
        txt = ""
        modified = False
        ht = self.host_type()
        found = False
        if ht in ("Linux", "Darwin"):
            with open( self.ACTIVATE_SH, "rt" ) as f:
                lines = f.readlines()
            result = []
            for tmp in lines:
                tmp = tmp.rstrip()
                if tmp.startswith("source "):
                    # the old source might be pointing at a different path
                    # So we look for the 'basename' not the abs path.
                    if os.path.basename(str(self.PYTHON_VARS_SH)) in tmp:
                        found = True
                        # The old one might be a different 'source' path
                        tmp = "source %s" % self.PYTHON_VARS_SH
                result.append(tmp)
            if not found:
                result.append("source %s" % self.PYTHON_VARS_SH)
            with open( self.ACTIVATE_SH, "wt" ) as f:
                print("Updating: %s" %  self.ACTIVATE_SH )
                f.write( "\n".join(result) )
                f.write("\n")
            # make it executable
            os.chmod( self.ACTIVATE_SH, 0o777)
            return
        assert( ht == "Windows")
        with open( self.ACTIVATE_BAT, "rt" ) as f:
            lines = f.readlines()
        result = []
        for tmp in lines:
            tmp = tmp.rstrip()
            if tmp.startswith( "call " ):
                if os.path.basename(str(self.PYTHON_VARS_BAT)) in tmp:
                    found = True
                    tmp = "call %s" % self.PYTHON_VARS_BAT
            result.append( tmp )
        if not found:
            result.append( "call %s" % self.PYTHON_VARS_BAT )
        with open( self.ACTIVATE_BAT, "wt" ) as f:
            f.write( "\n".join(result) )
            f.write("\n")
        found = False
        with open( self.ACTIVATE_PS1, "rt" ) as f:
            lines = f.readlines()
        for tmp in lines:
            tmp = tmp.rstrip()
            if tmp.startswith("."):
                if os.path.basename(str(self.PYTHON_VARS_PS1)) in tmp:
                    found = True
                    tmp = ". %s" % self.PYTHON_VARS_PS1
                result.append(tmp)
        if not found:
            result.append(". %s" % self.PYTHON_VARS_PS1 )
        with open( str(self.PYTHON_VARS_PS1), "wt" ) as f:
            f.write( "\n".join(result) )
            f.write('\n')
        return
