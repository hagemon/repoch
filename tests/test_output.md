## Overview

* README.md
* cmd/main.go
* internal/core/apps.go
### Purpose and Scope

The jetbra-free project is a cross-platform web application that serves as a license generator and activation tool for JetBrains IDEs. This system provides an automated solution for generating RSA-signed licenses and modifying IDE configuration files to enable full functionality of JetBrains development tools.

This document provides a high-level overview of the system architecture, core components, and technology stack. For detailed build instructions, see Building the Application. For information about the web interface components, see Web Interface. For development setup and dependency management, see Development Guide.

### System Architecture

The jetbra-free application is built as a self-contained Go web server using the Gin framework. The system consists of several key modules that work together to provide license generation and IDE activation capabilities.

#### High-Level Component Overview



#### Request Flow and Handler Mapping



### Technology Stack and Dependencies

The application is built using modern Go technologies with a focus on cross-platform compatibility and self-contained deployment.

#### Core Technology Components



### Key System Capabilities

#### IDE Catalog and License Generation

The system maintains a catalog of supported JetBrains IDEs with their specific product codes and activation requirements. Each IDE entry includes metadata such as icons, descriptions, and current crack status.

| Component | File Location | Primary Function |
| --- | --- | --- |
| IDE Catalog | `internal/core/apps.go` | Displays available IDEs with icons and metadata |
| License Generator | `internal/core/license.go` | Creates RSA-signed license strings |
| Plugin Manager | `internal/core/plugins.go` | Fetches and caches JetBrains plugin data |
| Crack Handler | `internal/core/crack.go` | Modifies IDE configuration files |



#### Self-Contained Deployment

The application uses go-bindata to embed all static assets directly into the compiled binary, creating a single executable file that contains:


* HTML templates for the web interface
* CSS stylesheets and JavaScript files
* JetBrains IDE icons in SVG format
* Configuration templates and certificates
This approach ensures the application can run without external dependencies on the target system.



#### Cross-Platform Build Support

The project includes dedicated build systems for different operating systems:


* Unix/Linux/macOS: Makefile with targets for building, running, and cleaning
* Windows: build.ps1 PowerShell script for Windows-specific builds
* Multi-architecture: Support for amd64 and arm64 architectures across platforms


#### Security and Certificate Management

The system includes a certificate management subsystem that generates self-signed certificates for license validation. This enables the application to create authentic-looking licenses that can be recognized by JetBrains IDEs.



For detailed information about specific subsystems, see the following pages:

  * Application startup and routing: Application Entry Point
  * Certificate generation process: Certificate Management System
  * License creation workflow: License Generation
  * IDE activation mechanisms: IDE Activation System
  * Build system details: Build System
