package com.rest.webservices.restful_web_services.helloworld;

import org.springframework.context.MessageSource;
import org.springframework.context.i18n.LocaleContextHolder;
import org.springframework.web.bind.annotation.*;

import java.util.Locale;

// REST API
@RestController
public class HelloWorldController {

	private MessageSource messageSource;

	public HelloWorldController(MessageSource messageSource) {
		this.messageSource = messageSource;
	}

	@RequestMapping(method = RequestMethod.GET,path ="/hello-world" )
	public String helloWorld()
	{
		return "Hello World";
	}
	
	@GetMapping(path ="/hello-world-bean" )
	public HelloWorldBean helloWorldBean()
	{
		return new HelloWorldBean("Hello World");
	}
	
	@GetMapping(path ="/hello-world/path-var/{name}")
	public HelloWorldBean helloWorldPathVar(@PathVariable String name)
	{
		return new HelloWorldBean(String.format("Hello World, %s", name));
	}

	@GetMapping(path = "/hello-world-internationalized")
	public String helloWorldInternationalized() {
		Locale locale = LocaleContextHolder.getLocale();
		return messageSource.getMessage("good.morning.message", null, "Default Message", locale);
		//return "Hello World V2";
	}

}
