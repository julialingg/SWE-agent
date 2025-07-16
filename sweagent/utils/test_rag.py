from sweagent.utils.rag_utils import retrieve_wcag_knowledge

# 模拟一个 issue 文本
mock_problem = """ Resolves a couple of issues with how focus is managed in the chips. Includes:
      _x000D_

      _x000D_

      ### fix(material/chips): chip grid not re-focusing first item_x000D_

      There was some logic that assumed that if a chip is the active item in the key
      manager, it must have focus. That''s incorrect since the active item isn''t
      reset on blur. This prevented the chip grid from re-focusing the first chip
      when the user tabs into it a second time._x000D_

      _x000D_

      These changes add a `focus` call whenever the grid receives focus._x000D_

      _x000D_

      Fixes #29785._x000D_

      _x000D_

      ### fix(material/chips): focus escape not working consistently_x000D_

      Fixes that the chip grid was using change detection to allow focus to escape
      on tab presses. That''s unreliable, because change detection might not be executed
      immediately. These changes fix the issue by changing the DOM node directly.


      ---


      ### Is this a regression?


      - [ ] Yes, this behavior used to work in the previous version


      ### The previous version in which this bug was not present was


      _No response_


      ### Description


      The focus indicator is not displayed for the chip grid when navigating through
      a MatChipGrid component the second and subsequent time.


      ### Reproduction


      StackBlitz link: https://stackblitz.com/run?file=package.json_x000D_

      Steps to reproduce:_x000D_

      1. Go to https://material.angular.io/components/chips/overview#chips-input_x000D_

      2. Tab through this MatChipGrid example_x000D_

      3. Click anywhere on the page to reset the focus_x000D_

      4. Tab through the example again_x000D_

      5. Notice that the focus indicator is not rendered around the chip grid the
      second time_x000D_



      ### Expected Behavior


      The focus indicator should always be displayed around the chip grid when navigating
      through.


      ### Actual Behavior


      The focus indicator is not rendered around the chip grid the second (and subsequent)
      time.


      ### Environment


      - Angular:_x000D_

      - CDK/Material: 18.2.5_x000D_

      - Browser(s): Chrome_x000D_

      - Operating System (e.g. Windows, macOS, Ubuntu): macOS_x000D_
 """

if __name__ == "__main__":
    print("🔍 Running mock RAG retrieval for accessibility issue...\n")
    rag_result = retrieve_wcag_knowledge(issue_text=mock_problem)
    print(rag_result)
