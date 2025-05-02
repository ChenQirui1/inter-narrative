import { useEffect, useState } from "react";
import "terminal.css";
import type { StoryRequest, StoryResponse, Beat } from "./types";

//basic tests

function App() {
  const [code, setCode] = useState("");
  const [codeEntered, setCodeEntered] = useState(false);
  const [form, setForm] = useState({ story: "", action: "" });
  const [response, setResponse] = useState({} as StoryResponse);
  const [error, setError] = useState("");

  // gameplay
  const [dice, setDice] = useState(0);
  const [action, setAction] = useState("");
  const [currentBeats, setCurrentBeats] = useState([] as Beat[]);
  const [currentStory, setCurrentStory] = useState([] as Beat[]);

  // trigger when new response is received
  // useEffect(() => {
  //   // if no response, return
  //   if (!response || response.beats.length === 0) return;

  //   console.log("response", response);
  //   // perform a dice roll
  //   setDice(Math.floor(Math.random() * response.beats.length));
  //   console.log("dice", dice);
  //   // select till the random index
  //   const selectedBeats = beats.slice(0, dice + 1);

  //   // add the selected beats to the current story
  //   setCurrentStory((prev) => [...prev, ...selectedBeats]);
  //   setCurrentBeats(selectedBeats);
  // }, [response]);

  const handleResponse = (response: StoryResponse) => {
    // const { story, beats } = response;
    // perform a dice roll
    const randomIndex = Math.floor(Math.random() * response.beats.length);
    console.log("index", randomIndex);
    setDice(randomIndex);
    // select till the random index
    const selectedBeats = response.beats.slice(0, randomIndex + 1);

    // add the selected beats to the current story
    setCurrentStory((prev) => [...prev, ...selectedBeats]);
    setCurrentBeats(selectedBeats);
  };

  // Handle code prompt submission
  const handleCodeSubmit = async (e: Event) => {
    e.preventDefault();
    if (code.trim() === "") {
      setError("Code is required.");
      return;
    }
    setError("");
    setCodeEntered(true);

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
    } catch (err) {
      setError(err.message || "Unknown error");
    }
  };

  // Handle form submission
  const handleSubmitPlayer = async (e) => {
    e.preventDefault();
    setError("");
    setResponse("");

    try {
      const storyRequest: StoryRequest = {
        story: JSON.stringify(currentStory),
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
    } catch (err) {
      setError(err.message || "Unknown error");
    }
  };

  return (
    <div className="App">
      <div className="terminal mx-5">
        {/* <h1>Submit Story & Action</h1> */}
        <div className="terminal-card">
          {!codeEntered ? (
            <form onSubmit={handleCodeSubmit}>
              <fieldset>
                <legend>Enter Access Code</legend>
                <div>
                  <label>
                    Code:
                    <input
                      type="text"
                      value={code}
                      onChange={(e) => setCode(e.target.value)}
                      required
                    />
                  </label>
                </div>
                <button type="submit">Continue</button>
              </fieldset>
              {error && (
                <div className="terminal-alert terminal-alert-error">
                  {error}
                </div>
              )}
            </form>
          ) : (
            <div className="terminal-card ">
              <header>Test Prompt</header>

              <div className="max-h-[50vh] overflow-auto">
                <p>
                  Lorem ipsum dolor sit amet consectetur adipisicing elit. Ea et
                  qui quis? Similique, optio. Perspiciatis explicabo suscipit
                  dolor et optio, at magnam fuga odit ut fugiat voluptate
                  dolore! Error, accusantium?
                </p>
                {currentStory.map((beat) => (
                  <p key={beat.beat}>{beat.description}</p>
                ))}
                {/* <p>aefaef</p> */}
              </div>
              <div>
                <form className="" onSubmit={handleSubmitPlayer}>
                  <fieldset>
                    <legend>Enter Action</legend>
                    <div className="form-group">
                      <label>
                        <input
                          type="text"
                          value={action}
                          onChange={(e) => setAction(e.target.value)}
                          placeholder="Enter action"
                        />
                      </label>
                    </div>
                    <button
                      type="submit"
                      className="btn btn-default"
                      role="button"
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

          {response && (
            <pre className="terminal-alert terminal-alert-success">
              <strong>Response:</strong>
              <br />
              {response.story}
            </pre>
          )}
          {error && codeEntered && (
            <div className="terminal-alert terminal-alert-error">{error}</div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
