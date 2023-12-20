import{g as i,u as c,o as l,c as u,a as e,w as _,b as s,d as a}from"./index-hnpzACsP.js";import{_ as d}from"./VContainers-h_r-JdSI.js";import{_ as m,a as f}from"./VHeader-TOPxYIWF.js";import{_ as o}from"./VStat-tMoju3Ko.js";import"./VWarningAlert-9tmtEAlV.js";const g=i`
  query getDashboard {
    version
    dockerVersion
    stackCount
    containers(stopped: false) {
      id
      name
      image
      service
      state
    }
  }
`,p={class:"mx-auto max-w-7xl"},h={class:"grid grid-cols-1 gap-4 sm:grid-cols-3"},k=a("h3",null,"Running Containers",-1),$={__name:"DashboardView",setup(v){const{result:t,loading:n,error:r}=c(g);return(x,D)=>(l(),u("div",null,[e(f,{title:"Dashboard"}),e(m,{loading:s(n),error:s(r),result:s(t),"result-key":"version"},{default:_(()=>[a("section",null,[a("div",p,[a("div",h,[e(o,{name:"Odooghost version",stat:s(t).version},null,8,["stat"]),e(o,{name:"Docker version",stat:s(t).dockerVersion},null,8,["stat"]),e(o,{name:"Stacks count",stat:s(t).stackCount},null,8,["stat"])])])]),a("section",null,[k,e(d,{containers:s(t).containers},null,8,["containers"])])]),_:1},8,["loading","error","result"])]))}};export{$ as default};
