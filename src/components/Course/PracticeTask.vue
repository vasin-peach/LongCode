<template>
  <div v-if="taskData" class="task-container">
    <div class="practiceTask row">
      <div class="taskDetail col-lg text-left">
        <div class="detail-nav">
          <div class="row">
            <div class="col-4 text-left">
              <router-link :to="{ name: 'practice' }" class="code-icon-backword">
                <i class="fa fa-backward" aria-hidden="true"></i> Back
              </router-link>
            </div>
            <div class="col-8 text-right">
              ||
              <strong>{{ taskData.name }}</strong> ||
            </div>
          </div>
        </div>

        <div class="detail-body pt-3">
          <div class="row">
            <div class="col">
              <div class="text-center">
                <h4>
                  <strong>{{ taskData.name}}</strong>
                </h4>
              </div>
              <hr style="border-color: #D94B3F" />
              <div style="word-break: break-all; letter-spacing: 0.5px;">
                <strong>Description:</strong>
                <div style="background: #e6e6e6; border-radius: 3px;">
                  <p
                    style="text-indent: 10px; padding: 5px; white-space: pre-wrap;"
                  >{{ taskData.detail }}</p>
                </div>
              </div>
              <br />
              <div>
                <div style="margin-bottom: 10px;">
                  <strong>Difficulty:</strong>
                  <span style="color: #4b4257">{{difficulty}}</span>
                </div>
                <div style="margin-bottom: 10px;">
                  <strong>Reward:</strong>
                  <span style="color: #4b4257">{{point}}</span>
                  <img
                    src="../../assets/icon/point.png"
                    style="width: 25px; border-radius: 50%; padding-bottom: 4px;"
                  />
                </div>
              </div>
              <br />
              <div>
                <strong>Input:</strong>
                <ul>
                  <li>
                    Main Function:
                    <strong
                      style="color: #4b4257; background: #e6e6e6; padding: 2px 5px;"
                    >{{ functionName }}</strong>
                  </li>
                  <li>
                    Argument:
                    <strong
                      style="color: #4b4257; background: #e6e6e6; padding: 2px 5px;"
                    >{{ argName }}</strong>
                  </li>
                  <li>
                    Time Limit:
                    <strong
                      style="color: #4b4257; background: #e6e6e6; padding: 2px 5px;"
                    >1000ms</strong>
                  </li>
                </ul>
              </div>
              <br />
              <div>
                <div style="margin-bottom: 10px;">
                  <strong>Testcase:</strong>
                </div>
                <div v-for="(testcase, count) in taskData.testcase">
                  <div
                    class="testcase-header"
                    width="75%"
                    style="cursor: pointer;"
                    data-toggle="collapse"
                    :data-target="'#' + taskData.createdAt + '-' + count"
                    aria-expanded="false"
                  >
                    <div class="row">
                      <div class="col-sm">Case {{ count+1}}</div>
                      <div class="col-sm text-right mr-2">
                        <span v-if="Math.round(taskLength / 2) <= count">
                          <i class="fa fa-lock" aria-hidden="true"></i>
                        </span>
                      </div>
                    </div>
                  </div>
                  <div
                    class="collapse testcase-body"
                    :id="taskData.createdAt + '-' + count"
                    v-if="count < Math.round(taskLength / 2)"
                  >
                    <ul>
                      <li>
                        <span v-for="x in testcase.input[0]">
                          Input:
                          <strong style="color: #4b4257; background: #e6e6e6;">
                            <span v-for="inputs in testcase.input">
                              <div v-for="(value, key) in inputs" style="padding: 0">
                                - {{key}}:
                                <strong
                                  style="color: #4b4257; background: #e6e6e6; padding: 2px 5px;"
                                >{{value}}</strong>
                              </div>
                            </span>
                          </strong>
                          <br />
                        </span>
                      </li>
                      <li>
                        Output:
                        <strong
                          style="color: #4b4257; background: #e6e6e6; padding: 2px 5px;"
                        >{{ testcase.output }}</strong>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>
              <br />
              <hr style="border-color: #D94B3F" />
              <br />
            </div>
          </div>
        </div>
      </div>
      <div class="taskCode col-lg text-left">
        <div class="code-nav">
          <div class="row">
            <div class="col-4 text-left">
              <span id="code-icon-reset" @click="taskLoad">
                <i class="fa fa-refresh" aria-hidden="true"></i> Reset
              </span>
            </div>
            <div class="col-8 text-right">
              <button
                class="btn btn-danger bg-salmon-1 pointer btn-sm"
                style="padding: 0px 10px;"
                @click="taskSubmit"
              >SUBMIT</button>
            </div>
          </div>
        </div>
        <div class="row code-container" style="margin: 0;">
          <div class="col" style="padding: 0;">
            <codemirror v-model="code" :options="editorOption" id="code-mirror"></codemirror>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// require active-line.js
require("codemirror/addon/selection/active-line.js");
// styleSelectedText
require("codemirror/addon/selection/mark-selection.js");
require("codemirror/addon/search/searchcursor.js");
// hint
require("codemirror/addon/hint/show-hint.js");
require("codemirror/addon/hint/show-hint.css");
require("codemirror/addon/hint/javascript-hint.js");
require("codemirror/addon/selection/active-line.js");
// highlightSelectionMatches
require("codemirror/addon/scroll/annotatescrollbar.js");
require("codemirror/addon/search/matchesonscrollbar.js");
require("codemirror/addon/search/searchcursor.js");
require("codemirror/addon/search/match-highlighter.js");
// keyMap
require("codemirror/mode/clike/clike.js");
require("codemirror/addon/edit/matchbrackets.js");
require("codemirror/addon/comment/comment.js");
require("codemirror/addon/dialog/dialog.js");
require("codemirror/addon/dialog/dialog.css");
require("codemirror/addon/search/searchcursor.js");
require("codemirror/addon/search/search.js");
require("codemirror/keymap/sublime.js");
// foldGutter
require("codemirror/addon/fold/foldgutter.css");
require("codemirror/addon/fold/brace-fold.js");
require("codemirror/addon/fold/comment-fold.js");
require("codemirror/addon/fold/foldcode.js");
require("codemirror/addon/fold/foldgutter.js");
require("codemirror/addon/fold/indent-fold.js");
require("codemirror/addon/fold/markdown-fold.js");
require("codemirror/addon/fold/xml-fold.js");

require("codemirror/mode/clike/clike.js");
require("codemirror/addon/edit/matchbrackets.js");
require("codemirror/addon/comment/comment.js");
require("codemirror/addon/dialog/dialog.js");
require("codemirror/addon/dialog/dialog.css");
require("codemirror/addon/search/searchcursor.js");
require("codemirror/addon/search/search.js");
require("codemirror/keymap/emacs.js");

import { mapState, mapMutations } from "vuex";
import firebase from "firebase";
import axios from "axios";
import swal from "sweetalert2";
import keys from "../../../config/index";
export default {
  name: "practiceTask",
  data() {
    return {
      currentEnrollX: null,
      currentEnrollI: null,
      taskId: this.$route.params.taskId,
      taskData: null,
      taskLength: 0,
      functionName: null,
      argName: null,
      fail: null,
      point: 60,
      difficulty: "easy",
      code: "hi",
      editorOption: {
        tabSize: 4,
        indentWithTabs: true,
        indentUnit: 4,
        styleActiveLine: false,
        lineNumbers: false,
        line: true,
        foldGutter: true,
        styleSelectedText: true,
        gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter"],
        highlightSelectionMatches: { showToken: /\w/, annotateScrollbar: true },
        mode: "text/x-python",
        hintOptions: {
          completeSingle: false
        },
        matchBrackets: true,
        showCursorWhenSelecting: true,
        theme: "hopscotch",
        autoCloseBrackets: true,
        extraKeys: { Ctrl: "autocomplete" },
        keyMap: "sublime"
      }
    };
  },
  computed: {
    ...mapState(["practiceList", "userAuth", "userData"])
  },
  mounted() {
    setTimeout(() => {
      this.editorOption.lineNumbers = true;
      this.editorOption.styleActiveLine = true;
    }, 3000);
  },
  created() {
    this.taskLoad();
  },
  updated() {
    this.screenFull();
  },
  methods: {
    ...mapMutations(["userDataFetch", "loading", "auth"]),
    taskLoad() {
      const this_ = this;
      firebase
        .database()
        .ref("/tasks")
        .orderByChild("createdAt")
        .equalTo(parseInt(this.taskId))
        .once("value")
        .then(function(snapshot) {
          for (var i in snapshot.val()) {
            this_.taskData = snapshot.val()[i];
            this_.taskLength = snapshot.val()[i].testcase.length;
            var testcase = this_.taskData.testcase[0].input;
            var functionName = this_.taskData.functionName;
            var func = [];
            var argName = [];
            var argValue = [];
            for (var y in testcase) {
              for (var x in testcase[y]) {
                argName.push(x);
              }
            }
            this_.functionName = functionName;
            this_.argName = argName;
            func.push(
              "def " +
                functionName +
                " (" +
                argName.join(", ") +
                "):\n\t#your code here"
            );
            this_.code = func.join("\n\n\n");

            // Created point
            this_.point =
              Math.round(
                ((this_.taskData.send / this_.taskData.pass) * 60) / 10
              ) * 10;
            if (!this_.point) {
              this_.point = 100;
            }

            // Created difficulty
            var percent = Math.round(
              (this_.taskData.pass * 100) / this_.taskData.send
            );
            if (percent > 90 || !percent) {
              var difficulty = "No data";
            } else if (percent < 90 && percent >= 70) {
              var difficulty = "Easy";
            } else if (percent < 70 && percent >= 50) {
              var difficulty = "Normal";
            } else if (percent < 50 && percent >= 30) {
              var difficulty = "Hard";
            } else {
              var difficulty = "Very Hard";
            }
            this_.difficulty = difficulty;
          }
        });
    },
    screenFull() {
      $(window).on("resize", function() {
        var screenHeight = $(window).height();
        var navbarHeight = $(".navbar").height();
        var fullHeight = screenHeight - navbarHeight;
        var halfHeight = fullHeight / 2;
        $(".practiceTask").css("min-height", fullHeight + "px");
        $(".code-container, .detail-body").css(
          "min-height",
          fullHeight - $(".code-nav").height() + "px"
        );
        var screenWidth = $(window).width();
        if (screenWidth <= 992 && screenWidth >= 767) {
          $(".practiceTask").css("margin-top", "-30px");
        } else {
          $(".practiceTask").css("margin-top", "-21px");
        }
      });
      var screenHeight = $(window).height();
      var navbarHeight = $(".navbar").height();
      var fullHeight = screenHeight - navbarHeight;
      var halfHeight = fullHeight / 2;
      $(".practiceTask").css("min-height", fullHeight + "px");
      $(".code-container, .detail-body").css(
        "min-height",
        fullHeight - $(".code-nav").height() + "px"
      );
      var screenWidth = $(window).width();
      if (screenWidth <= 992 && screenWidth >= 767) {
        $(".practiceTask").css("margin-top", "-30px");
      } else {
        $(".practiceTask").css("margin-top", "-21px");
      }
    },
    taskSubmit() {
      // Default
      const this_ = this;

      // Add this task in user data
      var query = "/users/" + this_.userData.authId;
      var updates = {};
      var taskUpdate = {};
      taskUpdate[this_.taskId] = { status: "doing" };
      updates[query + "/enroll"] = [taskUpdate];
      firebase
        .database()
        .ref(query)
        .once("value")
        .then(function(snapshot) {
          // never been
          if (!snapshot.val().enroll) {
            firebase
              .database()
              .ref()
              .update(updates);
            // task increase send
            var taskSend = firebase
              .database()
              .ref("tasks/" + this_.taskData.taskId + "/send");
            taskSend.transaction(function(send) {
              return send + 1;
            });
          } else {
            var enroll = snapshot.val().enroll;
            var enrollFound = true;

            // check current task is in user enroll
            for (var i in enroll) {
              for (var x in enroll[i]) {
                if (x == this_.taskId) {
                  enrollFound = false;
                }
              }
            }

            if (enrollFound) {
              // user enroll
              var newEnroll = [];
              newEnroll = newEnroll
                .concat(snapshot.val().enroll)
                .concat(taskUpdate);
              firebase
                .database()
                .ref(query + "/enroll")
                .set(newEnroll);

              // task increase send
              var taskSend = firebase
                .database()
                .ref("tasks/" + this_.taskData.taskId + "/send");
              taskSend.transaction(function(send) {
                return send + 1;
              });
            }
          }
        });

      this_.userDataFetch();
      const userCode = this.code;
      const taskData = this.taskData;
      const crossData = { userCode: userCode, taskData: taskData };
      // console.log(JSON.stringify(crossData))

      // Request data from python server
      var path = process.env.BACKEND_URI ? process.env.BACKEND_URI : 'http://localhost:5000';
      // Load loading animate
      this.loading(true);

      axios
        .post(path, crossData)
        .then(response => {
          // Close loading animate
          this.loading(false);
          var caseSet = [];
          var found = true;
          var pass = true;
          for (var i in response.data) {
            var currentData = response.data[i];
            if (currentData instanceof Array) {
              var caseName = "Case" + (currentData[0] + 1) + ": ";

              // SyntaxError
              if (currentData[1] == -2) {
                caseSet.push(
                  caseName +
                    ('<span style="color:orange">' + currentData[2] + "</span>")
                );
                pass &= false;
              } else {
                var re = currentData[1];
                pass &= re == 1 ? true : re == 0 ? false : false;
                caseSet.push(
                  caseName +
                    (re == 1
                      ? '<span style="color:green">Pass</span>'
                      : re == 0
                      ? '<span style="color:red">Wrong</span><br><span>Your Answer: ' +
                        currentData[2] +
                        " </span>"
                      : '<span style="color:red">Timeout</span>')
                );
              }

              // Code not found
            } else {
              found = false;
            }
          }
          if (found) {
            swal({
              title: "Task",
              type: pass ? "success" : "warning",
              html: caseSet.join("<br>")
            }).then(function() {
              if (pass) {
                var userTaskCheck = true;
                var userEnroll = this_.userData.enroll;
                for (var i in userEnroll) {
                  for (var x in userEnroll[i]) {
                    if (x == this_.taskId) {
                      for (var z in userEnroll[i][x]) {
                        if (userEnroll[i][x][z] == "finish") {
                          userTaskCheck = false;
                        }
                      }
                    }
                  }
                }
                if (userTaskCheck) {
                  swal({
                    title: "Reward",
                    imageUrl:
                      "https://grabkeys.net/storage/images/longcode/point.png",
                    html: "<h3>" + this_.point + "</h3>"
                  }).then(function() {
                    var userEnroll = this_.userData.enroll;
                    var currentEnrollX = null;
                    var currentEnrollI = null;
                    for (var i in userEnroll) {
                      for (var x in userEnroll[i]) {
                        if (x == this_.taskId) {
                          currentEnrollX = x;
                          currentEnrollI = i;
                        }
                      }
                    }
                    // update user enroll status
                    var enrollStatusQuery =
                      "users/" +
                      this_.userData.authId +
                      "/enroll/" +
                      currentEnrollI +
                      "/" +
                      currentEnrollX +
                      "/status";
                    var enrollStatus = firebase
                      .database()
                      .ref(enrollStatusQuery);
                    enrollStatus.transaction(function(status) {
                      return "finish";
                    });

                    // update task enroll pass
                    var taskPass = firebase
                      .database()
                      .ref("tasks/" + this_.taskData.taskId + "/pass");
                    taskPass.transaction(function(pass) {
                      return pass + 1;
                    });
                    // update user point
                    var userPoint = firebase
                      .database()
                      .ref("users/" + this_.userData.authId + "/point");
                    userPoint.transaction(function(point) {
                      return point + this_.point;
                    });
                    this_.userDataFetch();
                    this_.auth();
                  });
                } else {
                  swal({
                    title: "Redo",
                    html: "คุณจะไม่ได้คะแนน เรื่องจากคุณทำข้อนี้ไป",
                    type: "warning"
                  });
                }
              }
            });
          } else {
            swal({
              title: "Task",
              type: "error",
              html: "Code not found"
            });
          }
          if (pass) {
            // Update t
          }
        })
        .catch(error => {
          console.log("Error -> " + error);
        });
    }
  }
};
</script>

<style>
.CodeMirror-focused .cm-matchhighlight {
  background-image: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAIAAAACCAYAAABytg0kAAAAFklEQVQI12NgYGBgkKzc8x9CMDAwAAAmhwSbidEoSQAAAABJRU5ErkJggg==);
  background-position: bottom;
  background-repeat: repeat-x;
}
/* .cm-matchhighlight {background-color: lightgreen} */
.CodeMirror-selection-highlight-scrollbar {
  background-color: green;
}

.practiceTask {
  margin: 0 -15px;
  background: #444;
}
.practiceTask > div {
  padding: 0;
  margin: 0;
}
.taskDetail {
  /* z-index: 10 !important; */
  z-index: 1;
  background: #f2f2f2;
  min-height: 100%;
}
.detail-body {
  height: 500px;
  overflow-y: scroll;
  overflow-x: hidden;
}
.taskCode {
  background: #984b43;
  min-height: 100%;
}
.code-nav {
  background: #eac67a;
  padding: 5px 20px;
  box-shadow: 0 0 5px 0 #18121e;
}
#code-icon-reset,
.code-icon-backword {
  cursor: pointer;
  color: #4d4d4d;
  -webkit-transition: color 0.3s;
  -moz-transition: color 0.3s;
  transition: color 0.3s;
}
#code-icon-reset:hover,
.code-icon-backword:hover {
  color: #333333;
}
.detail-nav {
  background: #e7be65;
  padding: 5px 20px;
  box-shadow: 0 0 5px 0 #18121e;
}
.detail-body {
  padding: 5px 20px;
}
.detail-body li {
  padding: 10px;
}
.testcase-header {
  border-radius: 3px;
  padding: 5px;
  color: #dfdce3;
  background: #233237;
  margin-bottom: 5px;
}
.testcase-body {
  border-bottom-left-radius: 3px;
  border-bottom-right-radius: 3px;
  border: 1px dashed #d94b3f;
  border-style: none dashed dashed dashed;
  margin-bottom: 10px;
}

.CodeMirror {
  z-index: 1;
  min-height: 100%;
}
</style>
