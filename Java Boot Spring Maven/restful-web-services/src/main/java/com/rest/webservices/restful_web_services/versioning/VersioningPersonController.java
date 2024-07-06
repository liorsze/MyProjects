package com.rest.webservices.restful_web_services.versioning;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class VersioningPersonController {

    @GetMapping("/v1/person")
    public PersonV1 getFirstVersionPerson() {
        return new PersonV1("Bob Charl");
    }

    @GetMapping("/v2/person")
    public PersonV2 getSecondVersionPerson() {
        return new PersonV2(new Name("Bob", "Charl"));
    }
}
