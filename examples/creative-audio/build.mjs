import { build } from "esbuild";
import { copyFile, mkdir } from "node:fs/promises";
await mkdir("dist/adobe", { recursive: true });
await build({entryPoints:["adobe/app.js"], bundle:true,format:"esm",outfile:"dist/adobe/app.js",
  external:["https://express.adobe.com/static/add-on-sdk/sdk.js"],target:"es2022"});
for (const name of ["index.html","manifest.json"]) await copyFile("adobe/"+name,"dist/adobe/"+name);
await copyFile("canva/studio-chimes.mp3", "dist/adobe/studio-chimes.mp3");
await build({entryPoints:["canva/app.js"],bundle:true,format:"iife",outfile:"dist/canva/app.js",
  target:"es2022",minify:true,define:{"process.env.NODE_ENV":'"production"'},
  plugins:[{name:"inline-canva-styles",setup(b){b.onLoad({filter:/\.css$/},async a=>{
    const { readFile }=await import("node:fs/promises");
    return {contents:"const s=document.createElement('style');s.textContent="+JSON.stringify(await readFile(a.path,"utf8"))+";document.head.append(s);",loader:"js"};
  });}}]});

await copyFile("shared/messages.json", "dist/canva/messages_en.json");
