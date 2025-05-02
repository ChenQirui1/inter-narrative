
          <form onSubmit={handleSubmit}>
            <fieldset>
              <legend>Enter Data</legend>
              <div>
                <label>
                  Story:
                  <input
                    type="text"
                    name="story"
                    value={form.story}
                    onChange={handleChange}
                    required
                  />
                </label>
              </div>
              <div>
                <label>
                  Action:
                  <input
                    type="text"
                    name="action"
                    value={form.action}
                    onChange={handleChange}
                    required
                  />
                </label>
              </div>
              <button type="submit">Submit</button>
            </fieldset>
          </form>
        )}