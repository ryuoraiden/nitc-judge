/* Problem page: editor, run/submit, and the three-column diff that does the
   actual teaching when a test fails. */
(function () {
  "use strict";

  var P = window.JUDGE;
  var textarea = document.getElementById("code");
  var editor = null;
  var lastResult = null;

  /* ---------- editor ---------- */
  // CodeMirror comes from a CDN; if it is unreachable the plain textarea below
  // is still a perfectly usable editor, so the page degrades instead of breaking.
  if (window.CodeMirror) {
    editor = CodeMirror.fromTextArea(textarea, {
      mode: "text/x-csrc",
      theme: "material-darker",
      lineNumbers: true,
      indentUnit: 4,
      tabSize: 4,
      indentWithTabs: false,
      matchBrackets: true,
      autofocus: true,
      extraKeys: {
        "Ctrl-Enter": function () { doRun(); },
        "Ctrl-Shift-Enter": function () { doSubmit(); },
        Tab: function (cm) { cm.replaceSelection("    "); }
      }
    });
  } else {
    textarea.addEventListener("keydown", function (e) {
      if (e.key === "Tab") {
        e.preventDefault();
        var s = textarea.selectionStart;
        textarea.value = textarea.value.slice(0, s) + "    " + textarea.value.slice(textarea.selectionEnd);
        textarea.selectionStart = textarea.selectionEnd = s + 4;
      }
    });
  }

  function getCode() { return editor ? editor.getValue() : textarea.value; }
  function setCode(v) { if (editor) { editor.setValue(v); } else { textarea.value = v; } }

  /* ---------- tabs ---------- */
  document.querySelectorAll(".tabs").forEach(function (group) {
    group.querySelectorAll(".tab").forEach(function (tab) {
      tab.addEventListener("click", function () {
        var container = group.parentElement;
        group.querySelectorAll(".tab").forEach(function (t) { t.classList.remove("active"); });
        container.querySelectorAll(":scope > .pane").forEach(function (p) { p.classList.remove("active"); });
        tab.classList.add("active");
        var pane = document.getElementById(tab.dataset.pane);
        if (pane) pane.classList.add("active");
      });
    });
  });

  function showOutTab(id) {
    var tab = document.querySelector('.output .tab[data-pane="' + id + '"]');
    if (tab) tab.click();
  }

  /* ---------- resizers ---------- */
  function drag(handle, onMove) {
    handle.addEventListener("mousedown", function (e) {
      e.preventDefault();
      function move(ev) { onMove(ev); }
      function up() {
        document.removeEventListener("mousemove", move);
        document.removeEventListener("mouseup", up);
        document.body.style.userSelect = "";
        if (editor) editor.refresh();
      }
      document.body.style.userSelect = "none";
      document.addEventListener("mousemove", move);
      document.addEventListener("mouseup", up);
    });
  }
  var panelLeft = document.getElementById("panel-left");
  drag(document.getElementById("v-resizer"), function (e) {
    var w = Math.min(Math.max(e.clientX, 280), window.innerWidth - 360);
    panelLeft.style.width = w + "px";
  });
  var outputEl = document.getElementById("output");
  drag(document.getElementById("h-resizer"), function (e) {
    var h = Math.min(Math.max(window.innerHeight - e.clientY, 110), window.innerHeight - 220);
    outputEl.style.height = h + "px";
  });

  /* ---------- autosave ---------- */
  var saveTimer = null;
  function scheduleSave() {
    clearTimeout(saveTimer);
    saveTimer = setTimeout(function () {
      fetch("/api/draft/" + encodeURIComponent(P.problemId), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code: getCode() })
      }).catch(function () {});
    }, 1200);
  }
  if (editor) { editor.on("change", scheduleSave); } else { textarea.addEventListener("input", scheduleSave); }

  /* ---------- rendering ---------- */
  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  // Render text for the diff panes, marking the exact divergence point and
  // making trailing spaces visible - both are invisible bugs otherwise.
  function renderText(text, mark) {
    if (text === "" || text == null) return '<span class="empty-note">(empty)</span>';
    var lines = text.replace(/\r\n/g, "\n").split("\n");
    return lines.map(function (line, i) {
      var out = esc(line).replace(/ +$/, function (m) {
        return '<span class="miss">' + m.replace(/ /g, "·") + "</span>";
      });
      if (mark && mark[0] === i + 1) {
        var col = mark[1] - 1;
        var plain = esc(line);
        if (col <= line.length) {
          out = esc(line.slice(0, col)) +
                '<span class="miss">' + (esc(line.slice(col, col + 1)) || "·") + "</span>" +
                esc(line.slice(col + 1));
        } else {
          out = plain + '<span class="miss">·</span>';
        }
      }
      return out;
    }).join("\n");
  }

  var VERDICT_TEXT = {
    AC: "Accepted", WA: "Wrong Answer", TLE: "Time Limit Exceeded",
    RE: "Runtime Error", CE: "Compilation Error",
    OLE: "Output Limit Exceeded", OK: "Ran"
  };

  function renderResult(data, isSubmit) {
    lastResult = data;
    var host = document.getElementById("out-tests");

    if (!data.compile_ok) {
      host.innerHTML =
        '<div class="verdict-bar v-CE"><span>Compilation Error</span>' +
        '<span class="verdict-sub">gcc rejected your code &mdash; nothing ran</span></div>' +
        '<div class="log err">' + esc(data.compile_log) + "</div>";
      document.getElementById("out-compiler").innerHTML =
        '<div class="log err">' + esc(data.compile_log) + "</div>";
      showOutTab("out-tests");
      return;
    }

    document.getElementById("out-compiler").innerHTML = data.warnings
      ? '<div class="log warn">' + esc(data.warnings) + "</div>"
      : '<div style="color:var(--green);font-size:.83rem">Clean compile &mdash; no warnings from -Wall -Wextra.</div>';

    var label = VERDICT_TEXT[data.verdict] || data.verdict;
    var sub = isSubmit
      ? data.passed + "/" + data.total + " tests · " + data.max_ms + " ms"
      : "samples only · " + data.max_ms + " ms";
    var html = '<div class="verdict-bar v-' + data.verdict + '"><span>' + label +
               '</span><span class="verdict-sub">' + sub + "</span></div>";

    if (data.warnings) {
      html += '<div class="log warn" style="margin-bottom:.7rem">Compiler warnings (see Compiler tab) &mdash; ' +
              "code that passes with warnings is often passing by luck.</div>";
    }

    html += '<div class="pill-row">';
    data.tests.forEach(function (t, i) {
      html += '<button class="pill ' + (t.status === "AC" ? "ok" : "bad") + '" data-i="' + i + '">' +
              (t.is_sample ? "Sample " : "Test ") + (i + 1) + " · " + t.status +
              (t.visible ? "" : '<span class="lock">\u{1F512}</span>') + "</button>";
    });
    html += "</div><div id=\"test-detail\"></div>";
    host.innerHTML = html;

    host.querySelectorAll(".pill").forEach(function (pill) {
      pill.addEventListener("click", function () {
        host.querySelectorAll(".pill").forEach(function (p) { p.classList.remove("sel"); });
        pill.classList.add("sel");
        showDetail(data.tests[parseInt(pill.dataset.i, 10)]);
      });
    });

    var firstBad = data.tests.findIndex(function (t) { return t.status !== "AC"; });
    var pick = firstBad >= 0 ? firstBad : 0;
    if (data.tests.length) {
      host.querySelectorAll(".pill")[pick].classList.add("sel");
      showDetail(data.tests[pick]);
    }
    showOutTab("out-tests");
  }

  function showDetail(t) {
    var host = document.getElementById("test-detail");
    if (!t) { host.innerHTML = ""; return; }

    if (!t.visible) {
      host.innerHTML = '<div class="locked" style="padding:1.2rem">' +
        "Hidden test &mdash; verdict <strong>" + t.status + "</strong>" +
        (t.note ? " (" + esc(t.note) + ")" : "") + ".<br>" +
        "Its input is not shown, so you debug by reasoning about the code rather than by pattern-matching the answer key.<br>" +
        "Reproduce it in the Custom input tab.</div>";
      return;
    }

    if (t.status === "TLE" || t.status === "OLE" || t.status === "RE") {
      host.innerHTML = '<div class="log err">' + esc(t.note || t.status) + "</div>" +
        '<div class="diff-grid"><div class="diff-col"><div class="diff-head">Input</div>' +
        '<div class="diff-body">' + renderText(t.stdin) + "</div></div>" +
        '<div class="diff-col bad"><div class="diff-head">Output before it stopped</div>' +
        '<div class="diff-body">' + renderText(t.actual) + "</div></div>" +
        '<div class="diff-col"><div class="diff-head">Expected</div>' +
        '<div class="diff-body">' + renderText(t.expected) + "</div></div></div>";
      return;
    }

    var mark = t.status === "WA" ? t.diff_at : null;
    var where = mark ? " · first differs at line " + mark[0] + ", column " + mark[1] : "";
    host.innerHTML =
      (t.note ? '<div class="log warn" style="margin-bottom:.5rem">' + esc(t.note) + "</div>" : "") +
      '<div style="font-size:.75rem;color:var(--text-dim);margin-bottom:.2rem">' +
      t.duration_ms + " ms" + where + "</div>" +
      '<div class="diff-grid">' +
      '<div class="diff-col"><div class="diff-head">Input</div><div class="diff-body">' +
      renderText(t.stdin) + "</div></div>" +
      '<div class="diff-col ' + (t.status === "AC" ? "good" : "bad") + '">' +
      '<div class="diff-head">Your output</div><div class="diff-body">' +
      renderText(t.actual, mark) + "</div></div>" +
      '<div class="diff-col good"><div class="diff-head">Expected</div><div class="diff-body">' +
      renderText(t.expected, mark) + "</div></div></div>" +
      (t.stderr ? '<div class="log" style="margin-top:.5rem">stderr: ' + esc(t.stderr) + "</div>" : "");
  }

  /* ---------- actions ---------- */
  function busy(on) {
    document.getElementById("btn-run").disabled = on;
    document.getElementById("btn-submit").disabled = on;
  }

  function post(url, body) {
    return fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body || {})
    }).then(function (r) { return r.json().then(function (j) { return { ok: r.ok, data: j }; }); });
  }

  function doRun() {
    var custom = document.getElementById("custom-input").value;
    busy(true);
    document.getElementById("out-tests").innerHTML =
      '<div style="color:var(--text-dim);font-size:.83rem">Compiling and running…</div>';
    post("/api/run/" + encodeURIComponent(P.problemId), { code: getCode(), stdin: custom })
      .then(function (r) {
        if (custom.trim() !== "") { renderCustom(r.data); } else { renderResult(r.data, false); }
      })
      .catch(function (e) {
        document.getElementById("out-tests").innerHTML = '<div class="log err">' + esc(e) + "</div>";
      })
      .finally(function () { busy(false); });
  }

  function renderCustom(data) {
    var host = document.getElementById("custom-result");
    if (!data.compile_ok) {
      host.innerHTML = '<div class="log err">' + esc(data.compile_log) + "</div>";
      showOutTab("out-custom");
      return;
    }
    var t = data.tests[0] || {};
    host.innerHTML =
      '<div class="verdict-bar v-' + data.verdict + '"><span>' +
      (VERDICT_TEXT[data.verdict] || data.verdict) + '</span>' +
      '<span class="verdict-sub">' + (t.duration_ms || 0) + " ms</span></div>" +
      (t.note ? '<div class="log err" style="margin-bottom:.5rem">' + esc(t.note) + "</div>" : "") +
      '<div class="diff-col"><div class="diff-head">Output</div><div class="diff-body">' +
      renderText(t.actual) + "</div></div>" +
      (t.stderr ? '<div class="log" style="margin-top:.5rem">stderr: ' + esc(t.stderr) + "</div>" : "");
    showOutTab("out-custom");
  }

  function doSubmit() {
    busy(true);
    document.getElementById("out-tests").innerHTML =
      '<div style="color:var(--text-dim);font-size:.83rem">Running all tests…</div>';
    post("/api/submit/" + encodeURIComponent(P.problemId), { code: getCode() })
      .then(function (r) {
        renderResult(r.data, true);
        if (r.data.verdict === "AC") {
          setTimeout(function () { window.location.reload(); }, 1500);
        }
      })
      .catch(function (e) {
        document.getElementById("out-tests").innerHTML = '<div class="log err">' + esc(e) + "</div>";
      })
      .finally(function () { busy(false); });
  }

  document.getElementById("btn-run").addEventListener("click", doRun);
  document.getElementById("btn-submit").addEventListener("click", doSubmit);

  document.getElementById("btn-reset").addEventListener("click", function () {
    if (!confirm("Wipe the editor back to the starter stub? Your draft for this problem is discarded.")) return;
    post("/api/reset/" + encodeURIComponent(P.problemId)).then(function (r) { setCode(r.data.code); });
  });

  var hintBtn = document.getElementById("btn-hint");
  if (hintBtn) {
    hintBtn.addEventListener("click", function () {
      post("/api/hint/" + encodeURIComponent(P.problemId)).then(function (r) {
        document.getElementById("hints-box").innerHTML =
          r.data.hints.map(function (h) { return '<div class="hint">' + esc(h) + "</div>"; }).join("");
        if (r.data.hints.length >= r.data.total) hintBtn.remove();
      });
    });
  }

  var revealBtn = document.getElementById("btn-reveal");
  if (revealBtn) {
    revealBtn.addEventListener("click", function () {
      post("/api/reveal/" + encodeURIComponent(P.problemId)).then(function (r) {
        if (r.ok && r.data.ok) { window.location.reload(); }
        else { document.getElementById("reveal-msg").textContent = r.data.reason || "Still locked."; }
      });
    });
  }

  document.addEventListener("keydown", function (e) {
    if (e.ctrlKey && e.key === "Enter") { e.preventDefault(); e.shiftKey ? doSubmit() : doRun(); }
  });
})();
