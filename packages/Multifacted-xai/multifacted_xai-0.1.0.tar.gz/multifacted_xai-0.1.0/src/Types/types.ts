export interface AttrExplanation {
    "name": string, // name of the xai model, e.g. lime, shap, or any other user-defined name
    "score": number[]
    }

export interface CfExplanation {
    "name": string, // name of the xai model, e.g. Dice, or any other user-defined name,
    'original': (number|string)[],
    "delta": (number|string)[][]
    }

export interface RuleExplanation {
    "name": string, // name of the xai model
    "rule": (number|string)[][]
    }


export interface PDExplanation {
    "name": string, // name of the xai model
    "score": (number)[][] // 
    }


interface TableData  {
    type: "tabular",
    value: (string|number)[],
    headers: string[]
}

interface ImageData {
    type: "image",
    value: string // URL of the image
}

interface TextData {
    type: "text",
    value: string 
}

export interface AllExplanations {
    "independent_vars": {
        "names": Array< string >,
        'types': Array<'continuous' | 'categorical'>,
        "ranges": (string|number)[][],
        "values": (string|number)[]
    },
    "dependent_var": string,

    // "input_data": (string|number)[],
    "input_data": TableData | ImageData | TextData,
    
    "explanations": {
        "attribution"? : AttrExplanation[], // we can have multiple attribution-based explanations
        "cf"?: CfExplanation[],
        "rule"?: RuleExplanation[],
        'pd'?: PDExplanation[]
    }
}
