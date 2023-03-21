STUNNEL := stunnel

STUNNEL_BUILD := $(BUILD_HELPER_DIR)/$(STUNNEL)-build
STUNNEL_INSTALL := $(BUILD_HELPER_DIR)/$(STUNNEL)-install

$(STUNNEL_BUILD):
	$(BAZEL_BUILD) @$(STUNNEL)//:$(STUNNEL)
	$(BAZEL_BUILD) @$(STUNNEL)//:skel

$(STUNNEL_INSTALL): $(STUNNEL_BUILD)
	$(RSYNC) --chmod=u+w $(BAZEL_BIN)/$(STUNNEL)/$(STUNNEL)/bin $(DESTDIR)$(OMD_ROOT)/
	$(RSYNC) --chmod=u+w $(BAZEL_BIN)/$(STUNNEL)/$(STUNNEL)/lib $(DESTDIR)$(OMD_ROOT)/
	$(RSYNC) --chmod=u+w $(BAZEL_BIN)/$(STUNNEL)/$(STUNNEL)/share/bash-completion/completions/$(STUNNEL).bash $(DESTDIR)$(OMD_ROOT)/skel/etc/bash_completion.d/
	$(RSYNC) --chmod=u+w $(BAZEL_BIN)/$(STUNNEL)/skel/ $(DESTDIR)$(OMD_ROOT)/skel
	cd $(DESTDIR)$(OMD_ROOT)/skel/etc/rc.d/ && $(LN) -sf ../init.d/$(STUNNEL) 85-$(STUNNEL)
	chmod 664 $(DESTDIR)$(OMD_ROOT)/skel/etc/logrotate.d/$(STUNNEL)
	chmod 664 $(DESTDIR)$(OMD_ROOT)/skel/etc/$(STUNNEL)/server.conf
