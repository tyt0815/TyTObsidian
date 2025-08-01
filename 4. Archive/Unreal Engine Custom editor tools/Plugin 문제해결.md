---
dg-publish: true
---

`Warning: Plugin 'SuperManager' does not list plugin 'Niagara' as a dependency, but module 'SuperManager' depends on module 'Niagara'.`

위와 같이 플러그인이 다른 플러그인의 모듈에 의존할때, 플러그인에 list하지 않으면 경고가 발생한다.
`.uplugin`파일에 가서 아래와 같이 추가해 주면 warning이 사라진다.
```json
"Plugins": [
	{
		"Name": "EditorScriptingUtilities",
		"Enabled": true
	},
	{
		"Name": "Niagara",
		"Enabled": true
	}
]
```