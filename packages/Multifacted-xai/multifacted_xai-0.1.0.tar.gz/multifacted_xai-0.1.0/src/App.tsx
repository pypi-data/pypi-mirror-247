import React from "react";
import { ExpProvider, useExp } from "src/Context/ExpContext";

import InputData from 'src/Components/InputData'
import './App.css'
import { AllExplanations } from "src/Types/types";
import { Attribution, VarNames, PD , CF} from "src/Components/Explanations";

interface Props {
  exp?: AllExplanations
}
function App(props: Props) {
  const { exp } = props;

  return (
    <ExpProvider value={exp}>
      <InputData />
      <VarNames />
      <Attribution />
      <PD />
      <CF/>
    </ExpProvider>
  )
}

export default App
