(function () {
    var i = $.Object;
    var d = $.createClass($N("product.Translate"));
    i.extend(d, {
        info: "请输入要查询的单词",
        isInit: false,
        isPick: false,
        inputFlag: false,
        init: g,
        term: o,
        change: j,
        submit: f,
        request: n,
        get: h,
        show: b,
        pickClick: m,
        enablePick: c,
        disablePick: k,
        mouseup: l,
        getQueryWord: p,
        enableInput: a,
        disableInput: e
    });

    function g() {
        var r = this;
        var v = r.input = new $.Input({});
        var s = r.button = new $.Button({
            text: "英汉互译",
            click: $.Function.bind(r.submit, r)
        });
        var w = r.checkbox = new $.Checkbox({
            text: "即划即译",
            checked: true,
            checkedchange: $.Function.bind(r.pickClick, r)
        });
        var u = '<form name="tranFrom" onsubmit="$I(\'product.Translate\').submit();return false;" class="nui-toolbar"><div class="nui-toolbar-item">' + v.html() + '</div><div class="nui-toolbar-item">' + s.html() + '</div><div class="nui-toolbar-item"><div class="nui-toolbar-item-text">' + w.html() + '</div></div></form><div class="ni nui-txt-normal nui-scroll nui-scroll-hasShadow"><p class="ie" id="TranslateLoadingDiv" style="display:none">正在查询……</p><div id="TranslateNoneDiv" id="TranslateContentDiv" style="display:none;"></div><div id="TranslateContentDiv"></div><div class="jO" id="TranslateNoneDiv" style="display:none"></div></div>';
        var q = $.Link.html({
            link: "tran_download",
            noParam: true,
            target: "_blank"
        });
        r.msgbox = $.Msgbox.show({
            extcls: "qk",
            contentType: "wide",
            content: u,
            header: "有道海量词典",
            footer: q,
            ok: $.Function.bind(r.term, r, false),
            close: $.Function.bind(r.term, r, false),
            enter: $.Function.bind(r.submit, r),
            mask: false,
            okText: "关闭"
        });
        $.Component.setEvents();
        r.isInit = true;
        r.windows = [];
        r.pickClick();
        try {
            Log.record("tran")
        } catch (t) {}
    }

    function o(r) {
        var q = this;
        try {
            if (q.isInit) {
                if (q.isPick) {
                    q.disablePick()
                }
                q.isInit = false;
                q.windows = null;
                q.lastQuery = null;
                if (r) {
                    q.msgbox.close()
                }
            }
        } catch (s) {}
    }

    function j() {
        if (this.isInit) {
            this.term(true)
        } else {
            this.init()
        }
    }

    function f() {
        var q = this;
        var s = q.input.getEl().find("INPUT").dom;
        var t = $.String.trim(s.value);
        s.value = t;
        if (t.length == 0 || t == s.defaultValue) {
            q.disableInput();
            return
        }
        try {
            s.focus();
            s.select()
        } catch (r) {}
        if (t == q.lastQuery) {
            return
        } else {
            q.lastQuery = t
        }
        try {
            q.msgbox.getEl().find("#TranslateLoadingDiv").show()
        } catch (r) {}
        q.request(t, $.Function.bind(q.show, q))
    }

    function n(t, s) {
        var r = Uri.getUrl("tran_search", true);
        var q = "keyfrom=dictproxy&q=" + encodeURIComponent(t) + "&id=0&rnd=" + (new Date()).getTime() + "&url=" + encodeURIComponent(Uri.getUrl("tran_var", true) + "&q=" + encodeURIComponent(t));
        $.Ajax.jsonp(r + "?" + q, s)
    }

    function h(q) {
        return $.Eval.get("(" + q + ")")
    }

    function b(A, s) {
        var w = this;
        var F = w.get(s);
        var x = w.msgbox;
        x.getEl().find("#TranslateLoadingDiv").hide();
        var G = x.getEl().find("#TranslateContentDiv");
        var r = x.getEl().find("#TranslateNoneDiv");
        var q = $.String.encodeHTML(F.originalQuery);
        var C = "";
        if (F.customTranslation.content.length == 0 && F.yodaoWebDict.length == 0) {
            var K = new $.Link({
                link: "tran_noresult",
                target: "_blank",
                text: q
            });
            C += "				<p>抱歉，没有找到与您查询的“<em>" + q + '</em>”相符的字词。</p>				<ul class="nui-txt-tips">					<li>&middot; 请查看输入的字词是否有错误</li>					<li>&middot; 请在有道网页搜索中搜索“' + K.html() + "”</li>				</ul>			";
            r.dom.innerHTML = C;
            r.show();
            G.hide()
        } else {
            var z = [];
            if (F.customTranslation.content.length > 0) {
                var v = F.phoneticSymbol ? "[" + F.phoneticSymbol + "]" : "";
                var D = "";
                if (F.speech != null && F.speech != "") {
                    var u = Uri.getUrl("tran_flash", true) + F.speech;
                    D = '<object classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" id="tranSondSwf" style="width:17px;height:17px;margin-bottom:-4px;" codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=6,0,29,0"><param name="movie" value="' + u + '" /><embed src="' + u + '" quality="high" pluginspage="http://www.macromedia.com/go/getflashplayer" type="application/x-shockwave-flash" width="17" height="17" swLiveConnect=true id="tranSondSwf" name="tranSondSwf" allowScriptAccess="always" ></embed><param name="quality" value="high" /></object>'
                }
                var H = "";
                if (F.customTranslation.content) {
                    H = F.customTranslation.content.join("|")
                }
                var L = A == 1 ? '<p>来源于：<a href="' + F.customTranslation.source.url + '" target="_blank">' + F.customTranslation.source.name + "</a></p>" : "";
                z[z.length] = '					<h4 class="g-dialogBox-dict-content-title">&middot; 基本释义</h4>					<p>				';
                z[z.length] = '<strong class="g-dialogBox-dict-keyword">' + F.returnPhrase + "</strong> <span>" + v + "</span>";
                z[z.length] = D;
                z[z.length] = "					</p>					<p><strong>" + H + "</strong></p>					" + L + "				"
            }
            if (F.yodaoWebDict.length > 0) {
                var L = A == 1 ? "<p>来源于：有道</p>" : "";
                z[z.length] = '<h4 class="g-dialogBox-dict-content-title">&middot; 网络释义</h4>';
                z[z.length] = L;
                for (var J = 0, E = F.yodaoWebDict.length; J < E && J < 5; J++) {
                    var y = F.yodaoWebDict[J].key + "：";
                    var t = [];
                    for (var I = 0, B = F.yodaoWebDict[J].value.length; I < B; I++) {
                        t.push(F.yodaoWebDict[J].value[I])
                    }
                    z[z.length] = "<p><em>" + y + "</em><span>" + t.join(" | ") + "</span></p>"
                }
                z[z.length] = '<p><a href="' + F.yodaoLink + "&keyfrom=" + $S("product") + 'mail" target="_blank">完整搜索结果&gt;&gt;</a></p>'
            }
            G.dom.innerHTML = z.join("");
            G.dom.scrollTop = 0;
            r.hide();
            G.show()
        }
    }

    function m() {
        var q = this;
        if (q.checkbox.getChecked()) {
            q.enablePick()
        } else {
            q.disablePick()
        }
    }

    function c() {
        var s = this;
        $.Event.listen(document, "mouseup", s.mouseup);
        var r = s.windows;
        r[r.length] = window;
        q(document, true);
        s.isPick = true;

        function q(x, w) {
            try {
                var u = x.getElementsByTagName("IFRAME");
                for (var v = 0; v < u.length; v++) {
                    try {
                        var t = u[v].contentWindow;
                        $.Event.listen(t.document, "mouseup", s.mouseup);
                        r[r.length] = t;
                        if (w) {
                            q(t.document)
                        }
                    } catch (y) {}
                }
            } catch (y) {}
        }
    }

    function k() {
        var t = this;
        try {
            var r = t.windows;
            for (var s = 0; s < r.length; s++) {
                var q = r[s];
                try {
                    $.Event.unlisten(q.document, "mouseup", t.mouseup)
                } catch (u) {}
            }
        } catch (u) {}
        t.isPick = false;
        t.windows = []
    }

    function l() {
        var q = d;
        if (!q.isPick) {
            return
        }
        var r = q.getQueryWord();
        if (!r || r.length > 60) {
            return
        }
        q.enableInput(r)
    }

    function p() {
        var u = this;
        var w;
        if (!w) {
            try {
                var t = u.windows;
                for (var s = 0; s < t.length; s++) {
                    var q = t[s];
                    w = r(q, q.document);
                    if (w && w.length > 0) {
                        break
                    }
                }
                return w
            } catch (v) {
                return null
            }
        }
        return w;

        function r(y, x) {
            try {
                if (y.getSelection) {
                    return y.getSelection().toString()
                } else {
                    if (x.getSelection) {
                        return x.getSelection().toString()
                    } else {
                        if (x.selection) {
                            return x.selection.createRange().text
                        }
                    }
                }
            } catch (z) {}
            return null
        }
    }

    function a(s) {
        var q = this;
        var r = q.input.getEl().find("INPUT").dom;
        r.focus();
        if (s) {
            r.value = s;
            q.submit()
        }
    }

    function e() {
        var q = this;
        q.input.getEl().find("INPUT").dom.blur()
    }
})();
