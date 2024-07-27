package com.springboot.learn_jpa_and_hibernate.course.springdatajpa;

import com.springboot.learn_jpa_and_hibernate.course.Course;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface CourseSpringDataJpaRepository extends JpaRepository<Course, Long> {
     List<Course> findByAuthor(String author);
}
