import { useState, useEffect, useRef } from "react";
import "terminal.css";
import "./App.css";
import type { StoryRequest, StoryResponse, Beat } from "./types";
import audioFile from "./assets/069b4730-b59f-4b02-b625-b6cd9e474bb6.mp3";
import { ReactTyped } from "react-typed";

//basic tests
function App() {
  const [code, setCode] = useState("");
  const [codeEntered, setCodeEntered] = useState(false);
  // const [form, setForm] = useState({ story: "", action: "" });
  const [formDisabled, setFormDisabled] = useState(true);
  const [_response, setResponse] = useState({} as StoryResponse);
  const [error, setError] = useState("");
  const [time, setTime] = useState(new Date());

  const [loading, setLoading] = useState(false);

  // gameplay
  const [dice, setDice] = useState(0);
  const [action, setAction] = useState("");
  const [_currentBeats, setCurrentBeats] = useState([] as Beat[]);
  // const [curentBeatCount, setCurrentBeatCount] = useState(0);
  const [currentStory, setCurrentStory] = useState([] as Beat[][]);

  //autoscroll
  const bottomRef = useRef<HTMLDivElement | null>(null);
  const [autoScroll, setAutoScroll] = useState(false);

  useEffect(() => {
    const intervalId = setInterval(() => {
      setTime(new Date());
    }, 1000); // Update every 1 second

    return () => clearInterval(intervalId); // Cleanup on unmount
  }, []);

  useEffect(() => {
    if (autoScroll) {
      const interval = setInterval(() => {
        if (bottomRef.current) {
          bottomRef.current.scrollIntoView({
            behavior: "smooth",
            block: "end",
          });
        }
      }, 1000); // every 1 second
      return () => clearInterval(interval); // cleanup on unmount
    }
  }, [autoScroll]);

  // function handleScroll() {
  //   if (!bottomRef) return;
  //   if (bottomRef.current) {
  //     bottomRef.current.scrollIntoView({ behavior: "smooth", block: "end" });
  //   }
  // }

  const handleComplete = () => {
    // // Hide the cursor when typing is finished
    // if (typed && typed.cursor) {
    //   typed.cursor.style.display = "none";
    // } else {
    //   // Fallback: hide by class name (if cursor ref not available)
    //   const cursor = document.querySelector(".typed-cursor");
    //   if (cursor) cursor.style.display = "none";
    // }

    setAction("");
  };

  function formatDate(date: Date) {
    const day = date.getDate();
    const month = date.getMonth() + 1; // Months are zero-indexed
    const year = date.getFullYear() + 200;
    let hour = date.getHours();
    const minute = date.getMinutes().toString().padStart(2, "0");
    const second = date.getSeconds().toString().padStart(2, "0");
    const ampm = hour >= 12 ? "PM" : "AM";
    hour = hour % 12;
    hour = hour ? hour : 12; // the hour '0' should be '12'

    return `${day}/${month}/${year}, ${hour}:${minute}:${second} ${ampm}`;
  }

  const handleResponse = (response: StoryResponse) => {
    // const { story, beats } = response;
    // perform a dice roll

    //stop loading
    setLoading(false);

    let randomIndex;

    if (dice) {
      randomIndex = Math.floor(Math.random() * response.beats.length + 3);
    } else {
      randomIndex = Math.floor(Math.random() * response.beats.length);
    }

    setDice(randomIndex);
    // console.log("index", randomIndex);
    // select till the random index
    console.log("dice: ", dice);
    const selectedBeats = response.beats.slice(0, randomIndex);

    if (dice > response.beats.length) {
      console.log(response.beats.length);
      // let story play out
      const updateBeats = [
        ...response.beats,
        { beat: -1, description: "You Died" },
      ];

      setCurrentStory((prev) => [...prev, updateBeats]);
      setCurrentBeats(updateBeats);

      // set game over
      console.log("Died");
      // time out for a while then reload the page
      // setTimeout(() => {
      //   window.location.reload();
      // }, 5000);
    } else {
      // add the selected beats to the current story
      setCurrentStory((prev) => [...prev, selectedBeats]);
      setCurrentBeats(selectedBeats);
      setFormDisabled(false);
    }
  };

  // Handle code prompt submission
  const handleCodeSubmit = async (e: any) => {
    e.preventDefault();
    if (code.trim() === "") {
      setError("Code is required.");
      return;
    }
    setError("");
    setCodeEntered(true);
    setLoading(true);

    try {
      const storyRequest: StoryRequest = {
        story: "",
        action: "",
        code,
      };
      const response = await fetch(
        "https://asylo9o87a.execute-api.ap-southeast-1.amazonaws.com/default/story_gen",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(storyRequest),
        }
      );

      if (!response.ok) {
        throw new Error("Server error or invalid response.");
      }

      const data: StoryResponse = await response.json();

      handleResponse(data);
      setResponse(data);
    } catch (err: any) {
      setError(err.message || "Unknown error");
    }
  };

  // Handle form submission
  const handleSubmitPlayer = async (e: any) => {
    e.preventDefault();
    setError("");
    setFormDisabled(true);
    setLoading(true);

    try {
      const storyRequest: StoryRequest = {
        story: JSON.stringify(currentStory.flat()),
        action: action,
        code: code,
      };
      const response = await fetch(
        "https://asylo9o87a.execute-api.ap-southeast-1.amazonaws.com/default/story_gen",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(storyRequest),
        }
      );

      if (!response.ok) {
        throw new Error("Server error or invalid response.");
      }

      const data = await response.json();
      handleResponse(data);
      setResponse(data);
    } catch (err: any) {
      setError(err.message || "Unknown error");
    }
  };

  return (
    <div className="App">
      <audio src={audioFile} autoPlay loop />
      <div className="terminal mx-5">
        {/* <h1>Submit Story & Action</h1> */}
        <div className="">
          {!codeEntered ? (
            <form onSubmit={handleCodeSubmit}>
              <fieldset>
                <legend>Enter Access Code</legend>
                <div className="form-group">
                  <label>Code:</label>
                  <input
                    type="text"
                    value={code}
                    onChange={(e) => setCode(e.target.value)}
                    required
                  />
                </div>
                <button className="btn btn-default" type="submit">
                  Continue
                </button>
              </fieldset>
              {error && (
                <div className="terminal-alert terminal-alert-error">
                  {error}
                </div>
              )}
            </form>
          ) : (
            <div className="terminal-card ">
              <header>GOR v1.2.1</header>

              <div className="">
                <p className="mx-5">
                  Welcome to your DEATH! <br />
                  {formatDate(time)} <br />
                  {loading ? (
                    <ReactTyped
                      strings={["loading..."]}
                      loop={true}
                      typeSpeed={40}
                      showCursor={false}
                    />
                  ) : (
                    <ReactTyped
                      strings={["initialised"]}
                      typeSpeed={40}
                      showCursor={false}
                    />
                  )}
                </p>

                <div className="max-h-[50vh] overflow-auto">
                  {/* {currentStory.map((beat) => (
                    <p key={beat.beat}>{beat.description}</p>
                  ))} */}

                  <p ref={bottomRef}>
                    {currentStory.map((chunk, index) => (
                      <p>
                        <ReactTyped
                          key={index}
                          typeSpeed={10}
                          strings={[
                            chunk
                              .map((beat) => beat.description)
                              .join("<br /><br />"),
                          ]}
                          onBegin={() => setAutoScroll(true)}
                          onStringTyped={() => setAutoScroll(false)}
                          onComplete={handleComplete}
                        />
                      </p>
                    ))}
                  </p>
                  {/* <div ref={bottomRef}></div> */}
                </div>
                {/* <p>aefaef</p> */}
              </div>
              <div>
                <form className="" onSubmit={handleSubmitPlayer}>
                  <fieldset>
                    <legend>What happened next?</legend>
                    <div className="form-group">
                      <label>
                        <input
                          type="text"
                          value={action}
                          onChange={(e) => setAction(e.target.value)}
                          placeholder="Enter"
                          disabled={formDisabled}
                        />
                      </label>
                    </div>
                    <button
                      type="submit"
                      className="btn btn-default"
                      role="button"
                      disabled={formDisabled}
                    >
                      Enter
                    </button>
                  </fieldset>
                </form>
                {error && (
                  <div className="terminal-alert terminal-alert-error">
                    {error}
                  </div>
                )}
              </div>
            </div>
          )}

          {/* {response && (
            <pre className="terminal-alert terminal-alert-success">
              <strong>Response:</strong>
              <br />
              {response.story}
            </pre>
          )}
          {error && codeEntered && (
            <div className="terminal-alert terminal-alert-error">{error}</div>
          )} */}
        </div>
      </div>
    </div>
  );
}

export default App;
