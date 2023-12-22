export const showVarValue = (varValue: string|number):string=>{
    if ( typeof varValue === 'string' ){
        return varValue;
    } else {
        return varValue.toFixed(2);
    }
}