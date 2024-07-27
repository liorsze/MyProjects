package com.springboot.learn_jpa_and_hibernate.course;

import com.springboot.learn_jpa_and_hibernate.course.springdatajpa.CourseSpringDataJpaRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class CourseCommandLineRunner implements CommandLineRunner {

//    @Autowired
//    private CourseJdbcRepository repository;

//    @Autowired
//    private CourseJpaRepository repository;

    @Autowired
    private CourseSpringDataJpaRepository repository;

    @Override
    public void run(String... args) throws Exception {
        repository.save(new Course(1,"Learn AWS","Jon A."));
        repository.save(new Course(2,"Learn Azure","Amanda B."));
        repository.save(new Course(3,"Learn Docker","Bob C."));

        repository.deleteById(2L);

        System.out.println(repository.findById(3L));

        System.out.println(repository.findAll());
        System.out.println(repository.findByAuthor("Bob C."));
    }
}
