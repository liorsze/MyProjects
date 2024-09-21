package com.proj.microservices.inventory;

import io.restassured.RestAssured;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.server.LocalServerPort;
import org.springframework.boot.testcontainers.service.connection.ServiceConnection;
import org.springframework.context.annotation.Import;
import org.testcontainers.containers.MySQLContainer;

import static org.hamcrest.Matchers.is;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

@Import(TestcontainersConfiguration.class)
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class InventoryServiceApplicationTests {

	@ServiceConnection
	static MySQLContainer mySQLContainer = new MySQLContainer("mysql:8.3.0");
	@LocalServerPort
	private Integer port;

	@BeforeEach
	void setup(){
		RestAssured.baseURI = "http://localhost";
		RestAssured.port =port;
	}
	static {
		mySQLContainer.start();
	}

	@Test
	void shouldReadInventoryFalseResponse() {
		var negativeResponse = RestAssured.given()
				.when()
				.get("api/inventory?skuCode=iphone_15&quantity=105")
				.then()
				.log().all()
				.statusCode(200)
				.extract().response().as(Boolean.class)
				;
		assertFalse(negativeResponse);
	}

	@Test
	void shouldReadInventoryTrueResponse() {
		var Response = RestAssured.given()
				.when()
				.get("api/inventory?skuCode=iphone_15&quantity=100")
				.then()
				.log().all()
				.statusCode(200)
				.extract().response().as(Boolean.class)
				;
		assertTrue(Response);
	}

}
